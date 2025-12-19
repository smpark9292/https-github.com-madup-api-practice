import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np
from scipy import stats

# 한글 폰트 설정 (Windows 환경)
plt.rcParams['font.family'] = 'Malgun Gothic'
plt.rcParams['axes.unicode_minus'] = False

# 데이터 로드
df = pd.read_csv('discount_sales_data.csv', encoding='utf-8')

# 데이터 확인
print("=== 데이터 정보 ===")
print(df.head())
print("\n=== 기초 통계 ===")
print(df[['할인율', '매출액']].describe())

# 상관계수 계산
correlation = df['할인율'].corr(df['매출액'])
print(f"\n=== 상관분석 결과 ===")
print(f"할인율과 매출액의 상관계수: {correlation:.4f}")

# Pearson 상관계수와 p-value
pearson_corr, p_value = stats.pearsonr(df['할인율'], df['매출액'])
print(f"Pearson 상관계수: {pearson_corr:.4f}")
print(f"P-value: {p_value:.6f}")

if p_value < 0.05:
    print("→ 통계적으로 유의미한 상관관계가 있습니다 (p < 0.05)")
else:
    print("→ 통계적으로 유의미한 상관관계가 없습니다 (p >= 0.05)")

# 할인율별 평균 매출액
discount_avg = df.groupby('할인율')['매출액'].agg(['mean', 'count']).reset_index()
print("\n=== 할인율별 평균 매출액 ===")
print(discount_avg)

# 시각화
fig, axes = plt.subplots(2, 2, figsize=(15, 12))

# 1. 산점도 + 회귀선
ax1 = axes[0, 0]
ax1.scatter(df['할인율'], df['매출액'], alpha=0.6, s=100)
z = np.polyfit(df['할인율'], df['매출액'], 1)
p = np.poly1d(z)
ax1.plot(df['할인율'], p(df['할인율']), "r--", linewidth=2, label=f'회귀선 (y={z[0]:.0f}x+{z[1]:.0f})')
ax1.set_xlabel('할인율 (%)', fontsize=12)
ax1.set_ylabel('매출액 (원)', fontsize=12)
ax1.set_title(f'할인율 vs 매출액 산점도\n상관계수: {correlation:.4f}', fontsize=14, fontweight='bold')
ax1.legend()
ax1.grid(True, alpha=0.3)

# 2. 할인율별 평균 매출액 막대그래프
ax2 = axes[0, 1]
colors = ['#FF6B6B', '#4ECDC4', '#45B7D1', '#FFA07A', '#98D8C8']
bars = ax2.bar(discount_avg['할인율'].astype(str) + '%', discount_avg['mean'], 
               color=colors, edgecolor='black', linewidth=1.5)
ax2.set_xlabel('할인율', fontsize=12)
ax2.set_ylabel('평균 매출액 (원)', fontsize=12)
ax2.set_title('할인율별 평균 매출액', fontsize=14, fontweight='bold')
ax2.grid(True, alpha=0.3, axis='y')

# 막대 위에 값 표시
for bar in bars:
    height = bar.get_height()
    ax2.text(bar.get_x() + bar.get_width()/2., height,
             f'{int(height):,}원',
             ha='center', va='bottom', fontsize=9)

# 3. 카테고리별 할인율-매출액 관계
ax3 = axes[1, 0]
categories = df['카테고리'].unique()
category_colors = plt.cm.Set3(np.linspace(0, 1, len(categories)))

for i, category in enumerate(categories):
    category_data = df[df['카테고리'] == category]
    ax3.scatter(category_data['할인율'], category_data['매출액'], 
               label=category, alpha=0.7, s=80, color=category_colors[i])

ax3.set_xlabel('할인율 (%)', fontsize=12)
ax3.set_ylabel('매출액 (원)', fontsize=12)
ax3.set_title('카테고리별 할인율 vs 매출액', fontsize=14, fontweight='bold')
ax3.legend(loc='best')
ax3.grid(True, alpha=0.3)

# 4. 할인율별 매출액 박스플롯
ax4 = axes[1, 1]
df_boxplot = df.copy()
df_boxplot['할인율_str'] = df_boxplot['할인율'].astype(str) + '%'
boxplot = ax4.boxplot([df[df['할인율']==d]['매출액'].values for d in sorted(df['할인율'].unique())],
                       tick_labels=[str(int(d))+'%' for d in sorted(df['할인율'].unique())],
                       patch_artist=True,
                       boxprops=dict(facecolor='lightblue', alpha=0.7),
                       medianprops=dict(color='red', linewidth=2))
ax4.set_xlabel('할인율', fontsize=12)
ax4.set_ylabel('매출액 (원)', fontsize=12)
ax4.set_title('할인율별 매출액 분포 (박스플롯)', fontsize=14, fontweight='bold')
ax4.grid(True, alpha=0.3, axis='y')

plt.tight_layout()
plt.savefig('discount_sales_analysis.png', dpi=300, bbox_inches='tight')
print("\n시각화 결과가 'discount_sales_analysis.png'로 저장되었습니다.")

plt.show()

# 추가 분석: 카테고리별 상관계수
print("\n=== 카테고리별 상관계수 ===")
for category in df['카테고리'].unique():
    category_data = df[df['카테고리'] == category]
    if len(category_data) > 2:
        cat_corr = category_data['할인율'].corr(category_data['매출액'])
        print(f"{category}: {cat_corr:.4f}")


