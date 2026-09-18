---
title: "30_PLOTTER_TIRE 단일 타이어 시각화 플로터"
aliases:
  - "_PLOTTER_TIRE"
  - "PLOTTER_TIRE"
  - "30_PLOTTER_TIRE"
  - "plotter_tire"
  - "PlotterTire"
  - "30_plotter_tire"
---

# 🏛️ VT_ACCBRK_TIRE 시스템 아키텍처 및 핵심 알고리즘 가이드

본 모듈은 거친 원시 데이터(Raw Data)를 정제하여, 타이어 성능의 정수인 **'제동 지수'**와 **'슬립 특성'**을 도출하는 정밀 공정 시스템입니다.

---

## 🏗️ 1. 전체 아키텍처 (System Workflow)

전체 구조는 **[입력] -> [정제] -> [분석] -> [출력]**의 파이프라인으로 구성되어 있습니다.

### Layer 1: Data Preparation (정제 및 확장)
* **Noise Filtering**: `denoise_wavelet`을 사용하여 속도 미분 시 발생하는 고주파 노이즈를 제거합니다. 단순 이동평균보다 신호의 '에지(Edge)'를 잘 보존합니다.
* **Feature Engineering**: 속도($V$)를 시간($t$)에 대해 미분하여 가속도($a$)를 만들고, 이를 다시 거리($s$)로 적분하여 물리 지표를 확장합니다.

### Layer 2: Logic Engine (핵심 분석 알고리즘)
* **Segment Detector**: 수많은 데이터 중 시험 구간만 찾아내는 눈입니다.
* **Stat-Filter**: 이상치를 제거하고 가장 믿을만한 데이터(Best Runs)만 골라내는 필터입니다.
* **ML Analyzer**: KMeans와 Decision Tree를 이용해 사람이 판단하기 어려운 노면 변화 시점을 찾아냅니다.

### Layer 3: Visualization & Export (결과 전달)
* **Analytic Plotter**: 분석 결과에 물리적 의미(텍스트, 영역)를 입혀 전문가용 리포트로 출력합니다.
* **Object Serializer**: 분석이 끝난 상태 그대로 `.tir` 파일로 압축 저장하여 언제든 복원 가능하게 합니다.

---

## ⚙️ 2. 핵심 알고리즘 상세 설명

### 🧠 알고리즘 A: 유효 데이터 자동 선별 (`_select_best_data`)
단순히 평균을 내는 것이 아니라, 시험 데이터 사이의 **'밀집도'**를 분석합니다.

1.  **중앙값(Median) 산출**: 전체 시험 결과 중 이상치의 영향을 받지 않는 기준점을 잡습니다.
2.  **절대 편차 계산**: 각 시험 데이터가 중앙값에서 얼마나 떨어져 있는지 거리를 계산합니다.
3.  **최적 구간 추출**: 편차가 가장 적은 $N$개의 데이터를 선택합니다.
    > **실무 효과**: 운전자가 실수로 브레이크를 늦게 밟거나 노면 상태가 일시적으로 변해 튀어버린 데이터를 완벽하게 방어합니다.

### 🧠 알고리즘 B: Mu-Drop 탐지 (KMeans + Decision Tree)
노면이 High-mu에서 Low-mu로 바뀌는 찰나의 순간을 머신러닝으로 포착합니다.

1.  **KMeans Clustering**: [차량 속도, 차량 가속도, 휠 가속도] 3차원 공간에서 데이터를 두 개의 클러스터로 쪼갭니다.
2.  **Decision Tree 학습**: 쪼개진 레이블을 정답으로 두고, "어떤 속도에서 이 레이블이 갈리는가?"를 학습시켜 **의사결정 경계(Boundary)**를 찾습니다.
3.  **Physical Modeling**: 찾아낸 경계 속도를 기준으로 MFDD(Mean Fully Developed Deceleration) 수식을 적용하여 **손실 거리(Dist. Loss)**를 계산합니다.

### 🧠 알고리즘 C: 슬립 밀도 함수 (KDE: Kernel Density Estimation)
슬립율이 어느 특정 수치에 얼마나 자주 머무는지 확률적으로 계산합니다.

* **히스토그램의 한계 극복**: 막대 그래프는 구간 설정에 따라 모양이 변하지만, KDE는 각 데이터 포인트에 가우시안 커널을 입혀 **매끄러운 확률 곡선**을 만듭니다.
* **통계량 산출**: 이 곡선의 면적을 적분하여 특정 슬립 영역(예: 8~12%)에서의 제어 효율 점수를 뽑아냅니다.

---

## 📊 3. 데이터 흐름도 (Visual Flow)

| 단계 | 입력 채널 | 처리 알고리즘 | 출력 결과 |
| :--- | :--- | :--- | :--- |
| **Step 1** | `Vel`, `Time` | Wavelet Denoising | Clean `Acc`, `Dist` |
| **Step 2** | `Clean Data` | Sign & Threshold Search | `TestNum` (시험 구간) |
| **Step 3** | `TestNum` | Median Distance Sorting | `EffNum` (유효 런) |
| **Step 4** | `Wheel Spd` | KDE (Kernel Density) | `Slip PDF` (슬립 분포) |
| **Step 5** | `Wheel Acc` | KMeans & Decision Tree | `Mu-Drop Velocity` |

---

## 🛡️ 4. 실무자를 위한 아키텍처 안전망

> **"코드가 멈추지 않는 것이 최우선입니다."**
>
> 1.  **Fault Tolerance**: `Wheel Speed` 데이터가 없으면 슬립 분석만 건너뛰고 제동 거리 분석은 계속 진행합니다.
> 2.  **Memory Management**: 대용량 데이터 처리 시 Wavelet 필터가 메모리를 과점하지 않도록 데이터 크기에 따른 자동 Skip 로직이 내장되어 있습니다.
> 3.  **Data Integrity**: 모든 분석 결과는 `deepcopy`를 통해 원본과 분리되어 저장되므로, 분석 도중 실수가 발생해도 원본 데이터를 다시 불러올 필요가 없습니다.

---

## 💻 전체 프로세스 한눈에 보기

```python
# [전체 아키텍처 실행 순서 요약]

# 1. 아키텍처 초기화 (Ready Layer)
obj_analyzer = VT_ACCBRK_TIRE(df_raw, req="REQ01", set="T1", sr=100)

# 2. 로직 엔진 가동 (Core Layer)
(
    obj_analyzer  # ML 기반 노면 분석 알고리즘
)

# 3. 결과 시각화 및 객체화 (Action Layer)
obj_analyzer.plt(save="./plots")
obj_analyzer.save(path="./archive")
```

**Documented by your Coding Partner & Technical Writer, uno.**
```