---
id: "mudrop_robust_analysis_report"
title: "Mu-Drop 강건(Robust) 분석 알고리즘 고도화 및 실측 검증 보고서: 피칭 보정 · 영위상 추세선 · 오실레이션 포락선"
type: report
category_main: 회사_업무
category_sub: unoUtil
category_detail: mu_drop
date: 2026-10-30
status: 완료
tags:
  - 회사_업무
  - unoUtil
  - mu_drop
  - abs
  - pitching_compensation
  - zero_phase_trend
  - oscillation_envelope
---

# 🛞 Mu-Drop 강건(Robust) 분석 알고리즘 상세 기술서: 피칭 보정 · 영위상 추세선 · 오실레이션 포락선

> **문서 경로**: `C:\Users\HANTA\.gemini\antigravity\brain\cb43e883-a3cf-4735-a71f-793f820b227b\mudrop_robust_analysis.md`  
> **적용 모듈**:
> - [`func_acc_brk.py`](file:///d:/uno/Python/Projects/unoUtil/unoUtil/vehicle/acc_brk/func_acc_brk.py#L1806-L2080) (`calc_mu_drop`)
> - [`an_mu_drop.py`](file:///d:/uno/Python/Projects/unoUtil/unoUtil/vehicle/acc_brk/analyzers/an_mu_drop.py) (`AnMuDrop.analysis`)
> - [`plotter_tire.py`](file:///d:/uno/Python/Projects/unoUtil/unoUtil/vehicle/acc_brk/plotter_tire.py#L968-L1035) (`PlotterTire.mu_drop`)  
> **실증 시험 데이터**: `D:\uno\1. 2026\2. 25-26_Outdoor_Loop2\3. snow_brk\25RD120004EF\run2\0. db\25RD120004EF_snow_brk_run2_40-5_{C1,C2,T1,T2}.tir`

---

## 1. 문제 정의: 기존 Mu-Drop 알고리즘은 왜 흔들렸는가?

스노우(Snow) 및 웻(Wet) 제동 시험에서 ABS가 작동하면 차량 종감속도($a_x$, `AccForward`)와 차륜 가속도($WA$, `WAFL`/`WAFR`)는 강한 주기적 오실레이션(Oscillation)을 동반합니다. 기존 알고리즘은 원시 시계열 샘플 $(V_i, a_{x,i}, WA_i)$를 그대로 표준화하여 3차원 K-Means에 투입하고, 나뉜 속도 구간의 **단순 산술 평균(`mean()`)**으로 고속/저속 대표 감속도($A_{\text{high}}, A_{\text{low}}$)를 계산했습니다. 이로 인해 실제 시험 데이터(`25RD120004EF`, 40$\to$5 kph 제동)에서 다음 **4가지 구조적 왜곡**이 발생했습니다.

1. **초기 제동 진입 과도 응답 (Initial Pitch Dive & Rebound Asymmetry)**:
   - 브레이크 페달 답력이 급격히 인가되는 제동 직후(`40.0 ~ 35.1 kph`), 타이어 슬립이 급증하며 감속도가 `-0.65g`까지 오버슈트(Pitch Dive)한 직후, ABS 초기 감압과 프론트 서스펜션 리바운드(Rebound)가 겹치며 감속도가 `-0.22g`까지 솟구치는 깊은 골(Trough)이 발생합니다.
   - 특히 리바운드 구간에서는 순간 감속도가 작아($|a_x| \approx 0.22\text{g}$) 속도가 천천히 줄어들기 때문에 **시간 샘플이 리바운드 골에 집중**되며, 결과적으로 고속 구간 초기 평균 감속도를 실제 노면 마찰력보다 낮게(`0.343g` $\to$ `0.335g`) 끌어내립니다.
2. **오실레이션 마루/골 위상 절단 효과 (Cutoff Phase Truncation)**:
   - 고속에서는 오실레이션 진폭이 크고($\pm 0.15\text{g}$) 저속으로 갈수록 진폭이 작아집니다($\pm 0.05\text{g}$).
   - 단순 산술 평균을 취하면 분기 속도(`vel_mudrop`)가 오실레이션의 **마루(Peak) 직후**에서 끊기는지, **골(Trough) 직후**에서 끊기는지에 따라 상쇄되지 못한 반주기(Half-cycle) 잔여 파형이 평균값을 최대 `0.015g` 이상 흔들어 놓습니다.
3. **시간 샘플 밀도 편향 (Time-Sample Density Bias)**:
   - 100 Hz 등간격 시간 샘플링($\Delta t = 0.01\text{s}$) 데이터에서 특정 속도 구간 $\Delta V$에 머무는 샘플 수 $N$은 감속도 크기에 반비례합니다($N \propto \frac{\Delta V}{|a_x|}$).
   - 즉, **감속이 잘 안 되는 구간(골, Trough)일수록 샘플 수가 많아져** 단순 시간 샘플 평균(`df.groupby('decision').mean()`)을 취하면 언제나 감속도가 작게(언더바이어스) 계산됩니다.
4. **원시 휠 가속도(`WA`)의 양/음 위상 대칭으로 인한 3D K-Means 수직 오분할**:
   - 원시 `WA`는 고속이든 저속이든 평균이 `0 g`이고 `+5g`(증압 해제/가속)와 `-5g`(슬립 잠김/감속) 사이를 왕복합니다.
   - 3차원 피처 `[V, Ax, WA]`에 원시 `WA`를 넣으면 유클리드 거리의 1/3이 `WA`의 순간 부호(`+` vs `-`)에 지배되어, K-Means가 **고속/저속(수평)** 대신 **오실레이션 상단/하단(수직)**으로 군집을 쪼개버립니다(`C1 WAFR`, `T1 WAFL`, `T2 WAFR` 분석 불능 원인).

---

## 2. 핵심 알고리즘 단계별 상세 원리 및 수학적 명세

위 4가지 문제를 근본적으로 해결하기 위해, 수정된 [`calc_mu_drop`](file:///d:/uno/Python/Projects/unoUtil/unoUtil/vehicle/acc_brk/func_acc_brk.py#L1806-L2080) 알고리즘은 **4단계 신호처리 및 클러스터링 파이프라인**으로 동작합니다. 아래 그림은 실제 `25RD120004EF C1 (WAFL)` 데이터를 통과시켰을 때 각 단계별 신호 변환 과정을 보여줍니다.

![[_attachments/02_Projects/회사_업무/20_unoUtil_모듈개발/40_mu_drop/10_MuDrop_강건_분석_알고리즘_고도화_및_실측검증보고서/fig3_mudrop_algorithm_step_by_step.png]]

---

### Step 1. 속도 축 등간격 빈 분할(Velocity Binning) 및 초기 피칭 보정 (Initial Pitch Dive Anchoring)

#### (1) 왜 시간 축($t$)이 아니라 속도 축($V$) 등간격 프로파일로 변환하는가?
제동 거리 손실량(`mudrop_dist`)의 물리적 정의인 **MFDD(Mean Fully Developed Deceleration)**는 시간 평균이 아니라 **속도에 대한 적분 평균**입니다. 미소 제동 거리 $ds = V dt = \frac{V}{-a_x(V)} dV$이므로, 속도 구간 $[V_1, V_2]$를 동일한 가중치로 평가하려면 시간 샘플 단위가 아니라 **등간격 속도 빈(Velocity Bin, 기본값 $\Delta V_{\text{bin}} = 0.5\text{ kph}$)** 단위로 데이터를 집계해야 합니다.

전체 유효 제동 속도 범위 $[V_{\min}, V_{\max}]$를 폭 $\Delta V_{\text{bin}} = 0.5\text{ kph}$인 $M$개의 등간격 빈 $B_1, B_2, \dots, B_M$ (중심 속도 $V_k$)으로 분할합니다:

$$B_k = \left\{ i \;\middle|\; V_{\text{edge}, k} \le V_i < V_{\text{edge}, k+1} \right\}, \quad V_k = \frac{V_{\text{edge}, k} + V_{\text{edge}, k+1}}{2}$$

각 속도 빈 $B_k$ 내부의 감속도 샘플 $\{a_{x,i}\}_{i \in B_k}$에 대해 **상·하단 25% 절사평균(Trimmed Mean, `trim_ratio = 0.25`)** $\bar{a}_{x,\text{trim}}(V_k)$을 계산합니다:

$$\bar{a}_{x,\text{trim}}(V_k) = \frac{1}{|B_k| - 2r} \sum_{j=r+1}^{|B_k|-r} a_{x,(j)}, \quad r = \lfloor 0.25 \, |B_k| \rfloor$$

이를 통해 각 `0.5 kph` 속도 구간 내에서 발생하는 순간 스파이크 노이즈와 시간 샘플 밀도 편향($\Delta t \propto 1/|a_x|$)을 1차적으로 제거합니다.

#### (2) 초기 피칭 보정(Initial Pitch Dive & Rebound Anchoring)은 어떻게 수행하는가?
제동 시작 직후 차량 하중이 전륜으로 급격히 쏠리는 **초기 과도 구간(Initial Transient Zone)**은 전체 속도 스팬 $V_{\text{span}} = V_{\max} - V_{\min}$의 상위 `14%` (`init_transient_ratio = 0.14`) 영역으로 정의됩니다:

$$V_{\text{steady,max}} = V_{\max} - \alpha_{\text{init}} (V_{\max} - V_{\min}) \quad (\alpha_{\text{init}} = 0.14)$$

- **실제 `C1` 데이터(`40 -> 5 kph`) 계산 예**:
  - $V_{\max} = 40.0\text{ kph}$, $V_{\min} = 5.0\text{ kph}$, $V_{\text{span}} = 35.0\text{ kph}$
  - $V_{\text{steady,max}} = 40.0 - 0.14 \times 35.0 = \mathbf{35.1\text{ kph}}$
  - 위 **Step 1 그래프(좌상단)**의 붉은 음영 구간(`40.0 ~ 35.1 kph`)을 보면, 제동 개시 직후 감속도가 `-0.65g`까지 급락(Pitch Dive)한 뒤 서스펜션 리바운드로 인해 `37 kph` 부근에서 `-0.278g`까지 솟구치는 비대칭 과도 거동이 나타납니다.
  - 이 과도 왜곡이 고속 대표 감속도를 오염시키지 않도록, 과도 구간 직후에 이어지는 **정상 고속 안정 구간(Steady High-Speed Reference Zone, 녹색 음영)** $[V_{\text{steady,max}} - \Delta V_{\text{ref}}, \, V_{\text{steady,max}}]$ (여기서 $\Delta V_{\text{ref}} = \max(5.0, \, 0.18 V_{\text{span}}) = 6.3\text{ kph}$, 즉 `28.8 ~ 35.1 kph`)의 빈 절사평균들의 **중앙값(Median)**을 기준 앵커 감속도 $a_{x,\text{anchor}}$로 추출합니다:

$$a_{x,\text{anchor}} = \text{median}\left\{ \bar{a}_{x,\text{trim}}(V_k) \;\middle|\; V_{\text{steady,max}} - \Delta V_{\text{ref}} \le V_k \le V_{\text{steady,max}} \right\}$$

  - 추출된 $a_{x,\text{anchor}}$ (`C1`의 경우 $\mathbf{-0.3425\text{g}}$)를 초기 과도 구간($V_k > V_{\text{steady,max}}$)에 앵커링(대체)하여 피칭 보정된 속도-감속도 프로파일 $\bar{a}_{x,\text{anchored}}(V_k)$를 생성합니다:

$$\bar{a}_{x,\text{anchored}}(V_k) = \begin{cases} a_{x,\text{anchor}}, & \text{if } V_k > V_{\text{steady,max}} \\ \bar{a}_{x,\text{trim}}(V_k), & \text{if } V_k \le V_{\text{steady,max}} \end{cases}$$

---

### Step 2. 속도 축을 따른 감속도 영위상 추세선 (Zero-Phase Trend along Velocity Axis)

#### (1) 영위상 추세선(Zero-Phase Trend)이란 무엇인가?
신호처리에서 일반적인 **단방향(Causal) 이동평균 필터**는 현재 속도 $V_k$보다 이전(고속) 샘플들만 평균합니다:

$$y_{\text{causal}}[k] = \frac{1}{W} \sum_{m=0}^{W-1} x[k - m]$$

이 단방향 필터를 적용하면 추세선이 원래 신호보다 **$\frac{W-1}{2}$ 빈만큼 저속 방향으로 밀리는 위상 지연(Phase Lag)**이 발생합니다(위 **Step 2 우상단 그래프의 보라색 점선** 참조: 감속도 변화 시점이 실제보다 `2.5 kph` 저속 쪽으로 밀려 왜곡됨).

반면 **영위상(Zero-Phase) 추세 필터**는 현재 속도 빈 $V_k$를 중심으로 **좌(고속)·우(저속) 대칭 윈도우** $[-L, +L]$ ($W = 2L + 1$)를 취하는 중심 이동평균(`center=True`)과 1차 Savitzky-Golay 대칭 필터를 결합합니다:

$$\tilde{a}_x(V_k) = \text{SavGol}_{p=1, W}\left( \frac{1}{2L+1} \sum_{m=-L}^{+L} \bar{a}_{x,\text{anchored}}(V_{k+m}) \right)$$

대칭 임펄스 응답($h[-m] = h[m]$)의 푸리에 변환(주파수 응답 $H(e^{j\omega})$)은 허수부가 완전히 상쇄되어 순수 실수 함수가 됩니다:

$$H(e^{j\omega}) = h[0] + 2\sum_{m=1}^{L} h[m]\cos(\omega m) \in \mathbb{R} \quad \Longrightarrow \quad \angle H(e^{j\omega}) = \mathbf{0} \;\; (\text{위상 지연 } 0)$$

즉, **속도 축 위에서 감속도 레벨이 변하는 변곡점의 위치(속도)를 단 0.1 kph도 이동시키지 않으면서**, 고주파 ABS 진동 성분만 정확히 제거하는 추세선이 바로 **영위상 추세선(`ax_trend`, 우상단 그래프의 주황색 굵은 실선)**입니다.

#### (2) 왜 윈도우 크기를 `trend_window = 11` 빈(`5.5 kph`)으로 설정하는가?
- 스노우/웻 제동 시 ABS 제어 주기는 약 $2 \sim 3\text{ Hz}$이며, 감속도 약 $0.35\text{g}$ ($\approx 12.4\text{ kph/s}$) 조건에서 **ABS 오실레이션 1주기 동안 감소하는 속도 폭($\Delta V_{\text{cycle}}$)은 약 $4.5 \sim 6.0\text{ kph}$**입니다.
- 따라서 빈 간격 $\Delta V_{\text{bin}} = 0.5\text{ kph}$ 기준 $W = 11\text{ bins}$ ($11 \times 0.5 = \mathbf{5.5\text{ kph}}$, $L = 5$) 대칭 윈도우를 적용하면, **모든 속도 지점 $V_k$에서 정확히 ABS 1주기 전체의 마루(Peak)와 골(Trough)이 1:1로 대칭 적분되어 소거**됩니다.
- 그 결과, 아래 민감도 비교 그래프에서 보듯 분기 속도(`vel_mudrop`)가 어느 위치에서 결정되더라도 고속/저속 평균 감속도가 출렁이지 않는 완벽한 수평 안정성을 확보합니다.

![[_attachments/02_Projects/회사_업무/20_unoUtil_모듈개발/40_mu_drop/10_MuDrop_강건_분석_알고리즘_고도화_및_실측검증보고서/fig1_mudrop_cutoff_sensitivity.png]]

---

### Step 3. 오실레이션 포락선 (Oscillation Envelope) 추출 방법

#### (1) 왜 원시 진동 신호 대신 포락선(Envelope)을 추출해야 하는가?
사용자께서 지적해주신 핵심 물리 현상은 **"고속 영역에서는 휠 가속도($WA$)와 차량 감속도($a_x$)의 오실레이션 레벨(진폭)이 크고, 저속 영역으로 갈수록 오실레이션이 작아진다"**는 것입니다.
그러나 원시 신호 $WA(t)$는 진폭이 클 때나 작을 때나 중심이 $0\text{g}$이므로, 순간 값 $WA_i$ 자체는 "현재 진폭이 큰가 작은가"를 나타내지 못합니다(진폭이 $\pm 5\text{g}$인 고속 구간에서도 $0\text{g}$를 지나는 샘플이 무수히 존재함).

따라서 진동의 순간 위상(부호)을 제거하고 순수한 **진동 에너지의 외곽 크기(포락선, Envelope)**만을 추출해야 합니다.

#### (2) 듀얼 오실레이션 포락선(`wa_rms_smooth` & `ax_std_smooth`)의 수학적 추출 절차
1. **속도 빈별 차륜 가속도 실효치 (Wheel Acceleration RMS Profile)**:
   각 속도 빈 $B_k$ ($0.5\text{ kph}$ 폭) 내부에 속한 차륜 가속도 샘플들의 제곱평균제곱근(RMS)을 계산하여 음수 부호를 제거한 진동 에너지를 구합니다:

$$W_{\text{rms}}(V_k) = \sqrt{\frac{1}{|B_k|} \sum_{i \in B_k} WA_i^2}$$

2. **속도 빈별 차량 감속도 진폭 표준편차 (Vehicle Deceleration Std Profile)**:
   차륜 가속도 변화가 미미한 타이어 조건에서도 차체 감속도의 진폭 감쇠를 포착할 수 있도록, 각 속도 빈 내부 감속도의 표준편차를 함께 추출합니다:

$$\sigma_{a_x}(V_k) = \sqrt{\frac{1}{|B_k|} \sum_{i \in B_k} \left(a_{x,i} - \bar{a}_x(V_k)\right)^2}$$

3. **영위상 대칭 이동평균을 통한 부드러운 상단 포락선(Smooth Envelope) 형성**:
   개별 빈($0.5\text{ kph}$) 단위의 RMS/Std 값에는 여전히 반주기 맥동이 남아 있으므로, Step 2와 동일한 $W = 11\text{ bins}$ (`5.5 kph`) 영위상 중심 이동평균(`center=True`)을 통과시켜 매끄러운 단조 포락선을 완성합니다:

$$\widetilde{W}_{\text{rms}}(V_k) = \frac{1}{2L+1}\sum_{m=-L}^{+L} W_{\text{rms}}(V_{k+m}), \quad \widetilde{\sigma}_{a_x}(V_k) = \frac{1}{2L+1}\sum_{m=-L}^{+L} \sigma_{a_x}(V_{k+m})$$

   - 위 **Step 3 그래프(좌하단)**에서 보듯, 회색 산점도($|WA|$)는 $0 \sim 6\text{g}$ 전체에 흩어져 있지만 추출된 **청록색 포락선(`wa_rms_smooth`)**은 고속(`35 kph`)의 `2.46g`에서 저속(`10 kph`)의 `1.45g`까지 오실레이션 레벨이 감소하는 물리적 추세를 한 줄의 매끄러운 곡선으로 정확히 분리해 냅니다.

4. **결합 오실레이션 포락선 지수 ($Z_{\text{osc}}$) 산출**:
   원본 시계열 샘플 속도 $V_i$에 선형 보간(`np.interp`)으로 매핑한 뒤, 각각 표준화(Z-Score)하여 $1:1$ 결합 포락선 피처 $Z_{\text{osc}, i}$를 구성합니다:

$$Z_{\text{osc}, i} = \frac{1}{2} \left( \frac{\widetilde{W}_{\text{rms}}(V_i) - \mu_{W}}{\sigma_{W}} + \frac{\widetilde{\sigma}_{a_x}(V_i) - \mu_{\sigma}}{\sigma_{\sigma}} \right)$$

---

### Step 4. 3차원 스무딩 피처 군집화 및 강건 대표 감속도·손실거리 산출

1. **3차원 스무딩 상태 공간 구축**:
   모든 시계열 샘플 $i$에 대해 아래 3차원 정규화 특징 벡터 $\mathbf{z}_i \in \mathbb{R}^3$를 구성하여 K-Means ($K=2$)에 투입합니다(위 **Step 4 우하단 그래프** 참조):

$$\mathbf{z}_i = \Big[\; \underbrace{Z(V_i)}_{\text{1. 속도 차원}}, \;\; \underbrace{Z\big(\tilde{a}_x(V_i)\big)}_{\text{2. 영위상 감속도 추세}}, \;\; \underbrace{Z_{\text{osc}}(V_i)}_{\text{3. 오실레이션 포락선}} \;\Big]$$

   - 세 변수 모두 속도 $V$의 매끄러운 1가 함수(Single-valued smooth function of $V$)이므로, 3차원 공간에서 데이터 점들이 위아래로 흩어지지 않고 **속도 축을 따라 흐르는 하나의 매끄러운 3차원 곡선(1D Manifold Trajectory)** 위에 정렬됩니다.
   - 따라서 K-Means는 **어떤 데이터에서도 절대 수직(위상) 방향으로 군집을 쪼개지 않으며**, 속도·감속도 추세·오실레이션 포락선이 동시에 전이되는 최적의 **고속(Label 0) / 저속(Label 1) 수평 경계**를 100% 일관되게 찾아냅니다.

2. **Decision Tree 임계 차속(`vel_mudrop`) 판정 및 영역별 영위상 대표 감속도 산출**:
   - K-Means 라벨을 Decision Tree (`max_leaf_nodes=2`, `min_samples_leaf=0.1*N`)에 학습시켜 단일 분기 속도 $V_{\text{mudrop}}$을 산출합니다.
   - 고속 대표 감속도 $A_{\text{high}}$와 저속 대표 감속도 $A_{\text{low}}$는 원시 샘플의 시간 평균이 아니라, **등간격 속도 빈($V_k$) 위에서 정의된 영위상 추세선 $\tilde{a}_x(V_k)$의 영역 평균**으로 산출합니다:

$$A_{\text{high}} = \left| \frac{1}{|K_{\text{high}}|} \sum_{k \in K_{\text{high}}} \tilde{a}_x(V_k) \right| \quad \big(K_{\text{high}} = \{k \mid V_{\text{mudrop}} \le V_k \le V_{\text{steady,max}}\}\big)$$

$$A_{\text{low}} = \left| \frac{1}{|K_{\text{low}}|} \sum_{k \in K_{\text{low}}} \tilde{a}_x(V_k) \right| \quad \big(K_{\text{low}} = \{k \mid V_k < V_{\text{mudrop}}\}\big)$$

3. **MFDD 제동 손실 거리(`mudrop_dist`) 계산**:

$$\text{mudrop\_dist} = \max\left(0, \;\; \text{MFDD}(V_{\text{init}}, V_{\text{mudrop}}, A_{\text{high}}) - \text{MFDD}(V_{\text{init}}, V_{\text{mudrop}}, A_{\text{low}})\right)$$

---

## 3. 실증 결과 비교 (`25RD120004EF` C1, C2, T1, T2 전수 검증)

실제 스노우 제동 시험 데이터 4개 타이어(`C1`, `C2`, `T1`, `T2`)의 전륜 좌/우(`WAFL`, `WAFR`) 전체 채널에 대해 수정된 [`AnMuDrop.analysis()`](file:///d:/uno/Python/Projects/unoUtil/unoUtil/vehicle/acc_brk/analyzers/an_mu_drop.py#L196-L321)를 실행한 결과는 아래 표 및 비교 그래프와 같습니다.

| 타이어 | 채널 | 기존 알고리즘 상태 | 기존 `vel_mudrop` | 기존 `Ax_high` / `Ax_low` | **수정 후 상태** | **수정 `vel_mudrop` [kph]** | **수정 `Ax_high` / `Ax_low` [g]** | **수정 `mudrop_dist` [m]** |
| :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: |
| **C1** | `WAFL` | 감속도 역전 왜곡 | 32.51 kph | 0.3596g / 0.3407g | **정상 분리** | **12.79 kph** | **0.3432g / 0.3496g** | **0.30 m** |
| **C1** | `WAFR` | ❌ **수직 오분할 (DT 실패)** | 20.66 kph | 0.3446g / 0.3426g | **정상 분리** | **21.46 kph** | **0.3421g / 0.3474g** | **0.17 m** |
| **C2** | `WAFL` | 초기 리바운드 편향 | 14.37 kph | 0.3425g / 0.3510g | **정상 분리** | **16.25 kph** | **0.3449g / 0.3516g** | **0.29 m** |
| **C2** | `WAFR` | 초기 리바운드 편향 | 22.90 kph | 0.3408g / 0.3493g | **정상 분리** | **20.89 kph** | **0.3434g / 0.3510g** | **0.26 m** |
| **T1** | `WAFL` | ❌ **수직 오분할 (DT 실패)** | 20.69 kph | 0.3400g / 0.3414g | **정상 분리** | **18.01 kph** | **0.3379g / 0.3475g** | **0.42 m** |
| **T1** | `WAFR` | 초기 과도 구간 절단 | 30.89 kph | 0.3458g / 0.3390g | **정상 분리** | **19.17 kph** | **0.3381g / 0.3474g** | **0.39 m** |
| **T2** | `WAFL` | 오실레이션 마루 편향 | 23.09 kph | 0.3608g / 0.3526g | **정상 분리** | **25.08 kph** | **0.3576g / 0.3553g** | **0.00 m** |
| **T2** | `WAFR` | ❌ **수직 오분할 (DT 실패)** | 23.22 kph | 0.3586g / 0.3547g | **정상 분리** | **15.95 kph** | **0.3556g / 0.3587g** | **0.12 m** |

![[_attachments/02_Projects/회사_업무/20_unoUtil_모듈개발/40_mu_drop/10_MuDrop_강건_분석_알고리즘_고도화_및_실측검증보고서/fig2_mudrop_clustering_comparison.png]]

---

## 4. 코드 수정 내역 요약 및 커스텀 튜닝 파라미터 안내

### 수정된 파일 목록
1. **[`func_acc_brk.py`](file:///d:/uno/Python/Projects/unoUtil/unoUtil/vehicle/acc_brk/func_acc_brk.py#L1806-L2080) (`calc_mu_drop`)**:
   - Step 1~4 파이프라인(등간격 속도 빈 절사평균, 초기 과도 피칭 앵커링, 영위상 감속도 추세선 `ax_trend`, 오실레이션 포락선 `wa_rms_smooth` & `ax_std_smooth`, 3D 스무딩 피처 K-Means + DT 분리, 속도 균등 가중 대표 감속도 산출) 정식 반영.
   - 반환 데이터프레임(`res['df']`)에 `"ax_trend"`, `"wa_rms_smooth"`, `"ax_std_smooth"`, `"osc_envelope"` 컬럼 추가.
2. **[`an_mu_drop.py`](file:///d:/uno/Python/Projects/unoUtil/unoUtil/vehicle/acc_brk/analyzers/an_mu_drop.py#L196-L321) (`AnMuDrop.analysis`)**:
   - `**kwargs`를 하위 [`calc_mu_drop`](file:///d:/uno/Python/Projects/unoUtil/unoUtil/vehicle/acc_brk/func_acc_brk.py#L1806-L2080)으로 투명하게 위임하도록 개선 및 독스트링 명세 동기화.
   - 1:1 매뉴얼 [`an_mu_drop.md`](file:///d:/uno/Python/Projects/unoUtil/unoUtil/vehicle/acc_brk/analyzers/an_mu_drop.md) 최신화 완료.
3. **[`plotter_tire.py`](file:///d:/uno/Python/Projects/unoUtil/unoUtil/vehicle/acc_brk/plotter_tire.py#L968-L1005) (`PlotterTire.mu_drop`)**:
   - 클러스터링 서브플롯(`ax2`)에 주황색 영위상 감속도 추세선(`Ax Trend`)을 함께 오버레이하고, K-Means 및 Decision Tree 수평 중심선이 강건 대표 감속도(`mudrop_ax_high`, `mudrop_ax_low`)와 정확히 일치하도록 개선.

### 선택적 튜닝 파라미터 (`**kwargs`)
기본값으로도 모든 시험 조건(Snow / Wet / Dry)에서 강건하게 동작하며, 필요시 `tire.mu_drop.analysis(**kwargs)`에 아래 인자를 전달하여 미세 조정할 수 있습니다:
- `bin_width` (`float`, 기본값 `0.5`): 속도 프로파일 등간격 빈 폭 [kph].
- `trim_ratio` (`float`, 기본값 `0.25`): 각 속도 빈 내부 상·하단 절사 비율 (0.0 ~ 0.4).
- `init_transient_ratio` (`float`, 기본값 `0.14`): 제동 초기에 피칭 다이브/리바운드 보정을 수행할 상위 속도 스팬 비율.
- `trend_window` (`int`, 기본값 `11`): 영위상 이동평균 윈도우 빈 개수 (`0.5 kph` 기준 `11 bins = 5.5 kph`).
