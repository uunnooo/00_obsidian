---
id: "work_2026_snow_surface"
title: "00_2026 Snow Surface Characteristics 프로젝트 대시보드"
type: project
category_main: 회사_업무
category_sub: SnowSurface
date: 2026-09-10
status: 진행중
tags:
  - 회사_업무
  - SnowSurface
  - 노면특성
  - 데이터분석
  - 머신러닝
aliases:
  - "2026_Snow_Surface_Characteristics"
  - "00_2026_Snow_Surface_Characteristics_대시보드"
---

# 💼 2026 Snow Surface Characteristics (스노우 노면 특성 분석)

> [!ABSTRACT] ❄️ 프로젝트 개요
> 자연 기상 상태에서 급변하는 눈 트랙의 상태(눈 다져짐 깊이, 기온, 습도)를 수학적으로 격리하여, **어떤 날씨에서 테스트하든 타이어 고유의 성능 실력만 공정하게 뽑아내는 머신러닝 보정 시스템** 개발 과제입니다.

---

# 1. 노면 눌림량 계측 Infra

> [!NOTE] 📸 센서 지그 및 계측 인프라 구성
> 차량 휠 주변 및 외곽에 설치된 다채널 변위 센서를 통해 노면 높이 및 눈 눌림 깊이를 실측하는 인프라입니다.

![[_attachments/10_회사_업무/40_2026_Snow_Surface_센서_인프라.png|650]]

### ⚙️ 계측 및 데이터 처리 핵심
* **센서 위치에 따른 높이 옵셋 설정**:
  * 기구적 지그 길이와 센서별 장착 높이의 오차를 보정하기 위해 전체 계측 데이터 평균값 차이를 기준으로 옵셋 설정.
  * Out(외측)과 Tire(타이어부) 센서 간의 옵셋 매칭 및 차이를 산출하여 순수 눈 눌림량 정량치 추출.

---

## 🔗 연관 세부 프로젝트 및 핵심 알고리즘

* 🚀 **[[20_SnowBrakingPerformance_통합모듈_매뉴얼|SnowBrakingPerformance 통합 모듈 매뉴얼]]**
  * 노면 데이터/제동 평가(ACCBRK) 누적 등록, 3D 디지털 트윈, 차분 ML 보정 및 스펙 영향도 분석 마스터 클래스
* 📊 **[[10_노면특성_계측데이터_분석|노면특성 계측데이터 분석]]**
  * 다채널 센서 계측 로우데이터 기반 노면 특성 데이터베이스 구축
* 🧠 **[[30_Snow_제동성능보정_알고리즘|Snow제동성능보정 알고리즘 (Resources)]]**
  * **1단계 (시공간 디지털 트윈)**: 공간 예측 (Random Forest) ➡️ 시간 보간 (scipy interp1d) ➡️ VBOX GPS 격자 매칭
  * **2단계 (차분 머신러닝 보정)**: 타이어 고유 실력 소거(차분법) ➡️ KNN(3D 등고선 맵 시각화) + Random Forest(최종 정밀 보정 엔진)
* ❄️ **[[04_Resources/30_스노우_노면_공학/00_스노우_노면_공학_통합_색인|스노우 노면 공학 통합 지식 색인 (MOC)]]**