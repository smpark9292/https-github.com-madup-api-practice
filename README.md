# 할인율과 매출액 상관관계 분석

할인 전략의 효과를 데이터로 분석한 프로젝트입니다.

## 📊 분석 결과 요약

- **상관계수**: 0.0760 (통계적으로 유의미하지 않음)
- **최적 할인율**: 10~20%가 가장 효과적
- **인사이트**: 과도한 할인(50%)은 오히려 매출 감소

## 📁 파일 구성

- `discount_sales_data.csv`: 원본 데이터
- `analyze_discount_sales.py`: 분석 스크립트
- `discount_sales_analysis.png`: 시각화 결과

## 🚀 실행 방법

```bash
# 필요한 라이브러리 설치
pip install pandas matplotlib seaborn scipy

# 분석 실행
python analyze_discount_sales.py
```

## 📈 주요 발견

1. 할인율과 매출액은 선형적 관계가 아님
2. 카테고리별로 할인 효과가 다름
3. 패션/식품은 할인 효과가 크고, 전자기기는 오히려 역효과

