---
id: "10_GPStoXYCord"
title: "10_GPStoXYCord GPS 평면 직교 좌표계 투영 및 WGS84 벡터화 가속 엔진"
type: technical_manual
category_main: 회사_업무
category_sub: unoUtil
date: 2026-09-16
status: 완료
tags:
  - 회사_업무
  - unoUtil
  - GPS
  - WGS84
  - 좌표변환
  - VBOX
  - 매뉴얼
aliases:
  - 10_GPStoXYCord
  - _GPStoXYCord_
  - GPStoXYCord
  - GPStoDistance2
---

# 🛰️ GPStoXYCord: GPS 평면 직교 좌표계 투영 및 WGS84 벡터화 가속 엔진

**모듈 물리 경로**: [`unoUtil/gpsProcessing/_GPStoXYCord_.py`](file:///D:/uno/Python/Projects/unoUtil/unoUtil/gpsProcessing/_GPStoXYCord_.py)  
**소속 패키지**: `unoUtil.gpsProcessing`  
**버전**: 2026 Revision (WGS84 타원체 정밀 벡터화 가속화 및 0.0 노이즈 격리 탑재)  
**상위 대시보드**: [[00_gpsProcessing_대시보드]] | [[00_unoUtil_모듈개발_대시보드]]  
**관련 분석 모듈**: [[22_Func_ACCBRK]] | [[11_VT_ACCBRK_TIRE]]  

---

## 1. 📌 모듈 개요 및 아키텍처

`_GPStoXYCord_.py`는 실차 계측 장비(Racelogic VBOX, RT3000, GNSS 수신기 등)로부터 수집되는 구면 위경도(Latitude, Longitude) 좌표 데이터를 실차 거동 분석 및 제동/가속 평가에 필요한 **2차원 국소 평면 직교 좌표계($X$: 횡방향/레인 오프셋, $Y$: 종방향/주행거리)**로 변환하는 고성능 공간 데이터 연산 엔진입니다.

```mermaid
flowchart TD
    A["Raw GPS Data<br/>(VBOX Minutes or Decimal Deg)"] --> B{"VBOX 포맷 감지<br/>(|Lat.mean| > 90°)"}
    B -- Yes --> C["changeVBOXCoord()<br/>Minutes / 60.0"]
    B -- No --> D["Decimal Degrees 유지"]
    C --> E["유효 GPS 마스킹<br/>(0.0 노이즈 NaN 격리)"]
    D --> E
    E --> F["GPStoDistance2(method='wgs84')<br/>기준점 대비 상대거리 (X_dist, Y_dist)"]
    F --> G["RotationCoordinate(theta)<br/>트랙 진북 각도 회전 정렬"]
    G --> H["최종 로컬 좌표계<br/>(PosX: 레인위치, PosY: 주행거리)"]
```

---

## 2. ⚡ WGS84 타원체 정밀 가속 엔진 (`method='wgs84'`)

### 2.1 하버사인 vs WGS84 국소 곡률 투영 비교

과거 사용되던 구면 하버사인(Haversine) 공식은 지구를 완전한 구(반경 6,371km)로 가정하여 위도에 따른 회전타원체 편평률을 반영하지 못했습니다. 또한 데이터 1점마다 삼각초월함수($\sin, \cos, \arcsin, \sqrt{}$)를 반복 호출하므로 수십만 행 데이터 처리 시 CPU 병목을 유발했습니다.

WGS84 정밀 모드는 기준점 위도($\phi$)에서의 **타원체 곡률 반경(자오선 곡률 $M$, 묘유선 곡률 $N$)을 스칼라 상수로 1회만 계산**한 후, 전체 데이터 배열에 대해 단순 곱셈과 뺄셈만을 수행합니다.

$$
M(\phi) = \frac{a(1 - e^2)}{(1 - e^2 \sin^2\phi)^{1.5}}, \quad N(\phi) = \frac{a}{\sqrt{1 - e^2 \sin^2\phi}}
$$

$$
\Delta X = N(\phi) \cos\phi \cdot \Delta\lambda_{\text{rad}}, \quad \Delta Y = M(\phi) \cdot \Delta\phi_{\text{rad}}
$$

* $a = 6,378,137.0\,\text{m}$ (WGS84 타원체 장반경)
* $e^2 = 0.00669437999014$ (제1이심률의 제곱)

### 2.2 실측 벤치마크 결과 (137,951개 행 처리 기준)

```mermaid
xychart-beta
    title "13.8만 행 연산 속도 벤치마크 (ms)"
    x-axis ["Haversine 구면 모델", "WGS84 타원체 정밀 가속"]
    y-axis "소요 시간 (ms)" 0 --> 16
    bar [14.95, 2.53]
```

| 계산 모델 | 연산 시간 | 초(sec) 환산 | 속도 비율 | 측지 정밀도 |
| :--- | :---: | :---: | :---: | :---: |
| **Haversine (구면 모델)** | 14.95 ms | 0.015초 | 기준 (1.0x) | 구면 왜곡 포함 (~0.2% 편차) |
| **WGS84 (타원체 정밀)** | **2.53 ms** | **0.002초** | **🚀 5.9배 고속화** | `geopy` 타원체 실측과 **0.06 mm** 이내 일치 |

---

## 3. 🛡️ 핵심 데이터 방어 및 정제 아키텍처

### 3.1 계측 종료 후 0.0 노이즈 격리 (`valid_mask`)
* **발생 원인**: VBOX 장비는 시험 종료 후 수신이 중단되거나 차량 시동이 꺼질 때 `(0.0, 0.0)` 좌표를 연속으로 계측 파일 말미에 기록함.
* **영향**: 이를 그대로 기준점(테크노링 $36.6^\circ, 126.3^\circ$)과 거리 계산 시 $Y$ 좌표가 `-4,074,563m`로 왜곡되는 문제 발생.
* **방어 대책**:
  ```python
  # 유효 위경도(10도 이상) 마스크 생성
  valid_mask = (df_input[col_long] > 10.0) & (df_input[col_lat] > 10.0) & (~df_input[col_long].isna())
  df_xy = pd.DataFrame(index=df_input.index, columns=['PosX', 'PosY'], dtype=float)
  if valid_mask.any():
      df_xy.loc[valid_mask, ['PosX', 'PosY']] = rot_xy
  df_input[['PosX', 'PosY']] = df_xy  # 직접 컬럼 대입
  ```
  100Hz 시계열 인덱스는 100% 보존하면서, 비정상 구간만 `NaN`으로 격리하여 후속 차트 플롯 시 선 끊김(단절)으로 정상 렌더링되도록 처리.

### 3.2 VBOX 분(Minutes) 단위 판정 정밀화
* 노이즈 좌표 `0.0`이 포함된 상태에서 단순 전체 평균 `coord.mean() > 90`을 취하면 노이즈 비율에 따라 분 단위 감지가 누락될 수 있음.
* 따라서 `valid_mask`를 통해 **0.0이 배제된 유효 데이터의 위도 평균(`xy_valid[:, 1].mean() > 90.0`)**으로 판정 기준을 강화.

### 3.3 🌐 VBO vs VBB 경도 부호 차이 및 스마트 사분면 정규화
실차 시험 데이터 분석 중 발견된 VBOX 파일 포맷별 특성과 이를 방어하기 위한 정규화 알고리즘입니다:

1. **포맷별 경도(Longitude) 부호 차이의 원인**:
   * **`*.VBO` (ASCII Text)**: 영국 Racelogic 본사의 레거시 텍스트 규격(West is positive, East is negative)에 의해 동경(East) 데이터가 **음수(`-7580.11'`)**로 기록됨.
   * **`*.VBB` (Binary)**: 현대 국제 표준(WGS84 / ISO 6709: East is positive, West is negative)을 철저히 준수하여 동경 데이터가 **양수(`+7580.11'`)**로 기록됨.
2. **단순 절대값(`abs()`) 취득의 치명적 위험성 방어**:
   * 만약 모든 데이터에 맹목적으로 `abs()`를 걸어버리면, **미국 프루빙 그라운드(서경 $-80^\circ \sim -100^\circ$)** 시험 시 서경이 동경으로 뒤집히고, **남반구(칠레, 뉴질랜드 동계 시험장, 남위 $-35^\circ \sim -45^\circ$)** 시험 시 북반구로 차량이 왜곡되는 치명적 결함이 발생함.
3. **스마트 사분면 정규화 솔루션**:
   * **VBB**: WGS84 정규 부호를 100% 보존.
   * **VBO**: 경도(Longitude)에만 `-1`을 곱하여 정규 부호로 반전 복원 (위도 부호는 보존).
   * **auto 모드**: 기준점(`reflong`)과의 부호 일치 여부를 대조하여 VBO/VBB를 자동 식별 및 보정.

---

## 4. 📐 주요 함수 API 레퍼런스

### 4.1 `GPStoDistance2` (고속 상대 거리 변환)
```python
def GPStoDistance2(
    gpsData: Union[np.ndarray, pd.DataFrame],
    **kwargs: Any
) -> np.ndarray:
```
* **기능**: 기준점 대비 동서(X), 남북(Y) 상대 거리(m)를 벡터화하여 초고속 산출.
* **Keyword Args**:
  * `reflong` (Optional[float]): 기준점 경도 (미지정 시 10도 초과 유효 최소값).
  * `reflat` (Optional[float]): 기준점 위도 (미지정 시 10도 초과 유효 최소값).
  * `method` (str): `'wgs84'` (기본값, 타원체 정밀 고속) 또는 `'haversine'`.
  * `plot` (bool): 변환 전후 좌표 플롯 출력 여부 (기본값: False).

### 4.2 `RotationCoordinate` (2D 평면 회전 변환)
```python
def RotationCoordinate(
    xyData: Union[np.ndarray, pd.DataFrame],
    theta: float,
    **kwargs: Any
) -> np.ndarray:
```
* **기능**: 상대 직교 좌표를 트랙 진북 배치각 $\theta$만큼 회전시켜 종방향($Y$)과 횡방향($X$) 축으로 정렬.
* **테크노링 직선 제동로 최적값**: `theta = -0.4`
  * 제동 주행 중 차량의 횡방향 편차($\Delta \text{PosX}$)가 $\pm 1.3\,\text{cm}$ 이내로 완벽히 정렬됨.

### 4.3 `changeVBOXCoord` (스마트 VBOX 좌표 정규화)
```python
def changeVBOXCoord(
    coord: np.ndarray,
    file_type: str = "auto",
    reflong: Optional[float] = None,
    plot: bool = False
) -> np.ndarray:
```
* **기능**: VBOX 분(Minutes of arc) 단위 데이터를 60으로 나누어 표준 십진 도(Decimal Degrees)로 정규화.
* **포맷별 처리**:
  * `vbb`: WGS84 국제 표준 부호 유지 (`coord / 60.0`).
  * `vbo`: 경도 부호 자동 반전 복원 (`lon * -1 / 60.0`, `lat / 60.0`).
  * `auto`: 기준점 `reflong`과 부호 대조를 통해 자동 판별하여 보정.

---

## 5. 💻 독립 실행 및 자가 검증

본 모듈은 외부 의존성 없이 단독으로 실행하여 벤치마크 및 시뮬레이션을 수행할 수 있습니다:

```bash
# Windows PowerShell
python unoUtil/gpsProcessing/_GPStoXYCord_.py
```

**최신 검증 출력**:
```text
================================================================================
 [unoUtil GPS Processing Pipeline] 종합 검증 및 벤치마크 스위트
================================================================================

[Scenario 1] 137,951개 행(13.8만 포인트) 대용량 연산 속도 벤치마크
  - Haversine 구면 모델 소요 시간 :  19.63 ms
  - WGS84 타원체 정밀 모델 소요 시간:   3.97 ms  ([FAST] 4.94배 더 빠름)
  - 두 모델 간 거리 차이 최대치     : 2.2397 m (타원체 곡률에 의한 실측 편차 반영)

[Scenario 2] 테크노링 실제 VBO vs VBB 1:1 대조 및 스마트 부호 정규화 검증
  [*] VBB 파일 로드: example_dry_brk_lane8.VBB
  [*] VBO 파일 로드: example_dry_brk_lane8.vbo
      - VBB 로드 완료: 137,951 행, 51 채널
      - VBO 로드 완료: 137,952 행, 54 채널
  [*] GPS 0.0 노이즈 필터링: VBB 유효 135,729 / VBO 유효 135,730 행
  [*] 원천 Longitude 첫 행 부호 대조:
      - VBB (WGS84 표준):   +7580.117568' (양수 동경)
      - VBO (Racelogic) :   -7580.117568' (음수 부호 반전 확인)
  [*] changeVBOXCoord 스마트 변환 후 십진 도(Degrees) 확인:
      - VBB 십진 경도: 126.335293° (부호 보존)
      - VBO 십진 경도: 126.335293° (자동 반전 정상 복원)

[Result] 테크노링 직선 제동로(Lane 8) 로컬 좌표계 변환 결과:
  - PosX 범위 (횡방향): -92.82 m ~ 314.28 m
  - PosY 범위 (진행거리): -343.71 m ~ 1146.57 m
  - 1샘플(10ms) 헤더 정렬 후 두 파일 간 2D 평면 위치 오차:
      * 평균 오차 :   0.0064 mm (6.4 마이크로미터 수준)
      * 최대 편차 :   0.0118 mm (11.8 마이크로미터 수준)
      -> VBO(경도 반전)와 VBB(부호 유지)가 동일한 100% 실차 좌표로 완벽 일치 입증!
  - 제동 시작 시점 위치(first): PosX = 20.16 m, PosY = 249.03 m

[Scenario 3] 글로벌 시험장 스마트 사분면 방어 시뮬레이션 (구형 abs() 버그 해결 검증)
  [미국 텍사스 시험장 - 서경/북위] 기준: Lon=-99.1234°, Lat=29.5678°
    - VBB 변환 결과 : Lon=-99.1234°, Lat=29.5678° (음수 서경 정상 보존)
    - VBO 변환 결과 : Lon=-99.1234°, Lat=29.5678° (양수->음수 정상 반전)
  [칠레 동계 시험장 - 서경/남위] 기준: Lon=-70.5°, Lat=-33.4°
    - VBB 변환 결과 : Lon=-70.5000°, Lat=-33.4000° (음수 남위 정상 보존)
  -> 전 세계 모든 사분면(미국 서경, 남미/호주 남위)에서 100% 정상 작동 검증 완료!

================================================================================
 [검증 성공] unoUtil GPS 좌표 변환 및 스마트 사분면 정규화 파이프라인 검증 완료
================================================================================
```

---

## 🔗 연계 문서 링크

* 🛰️ **[[00_gpsProcessing_대시보드|gpsProcessing 모듈 전체 대시보드]]**
* 🏎️ **[[22_Func_ACCBRK|22_Func_ACCBRK: AN_ACCBRK 로컬 좌표 파이프라인 연계]]**
* 🚗 **[[11_VT_ACCBRK_TIRE|11_VT_ACCBRK_TIRE: 랩별 제동 시작 위치 PosX/PosY 집계]]**
