import pandas as pd
import seaborn as sns
import numpy as np
from sklearn.datasets import load_iris

iris = sns.load_dataset("iris")
print(iris)
print("=" * 30)

# 그래프 표시 
sns.set(style="ticks", color_codes=True)
g = sns.pairplot(iris, 
                 hue="species", 
                 palette="husl")


# 붓꽃 데이터 세트를 로딩합니다. 
iris = load_iris()

# iris.data는 Iris 데이터 세트에서 
# 피처(feature)만으로 된 데이터를 
# numpy로 가지고 있습니다. 
iris_data = iris.data
print(iris_data)

# iris.target은 붓꽃 데이터 
# 세트에서 레이블(결정 값) 
# 데이터를 numpy로 가지고 있습니다. 
iris_label = iris.target
print(iris_label)
print('iris target값:', list(set(iris_label)))
print('iris target명:', iris.target_names)
print("=" * 30)

# 붓꽃 데이터 세트를 자세히 보기 위해 
# DataFrame으로 변환합니다. 
iris_df = pd.DataFrame(data=iris_data, 
                       columns=iris.feature_names)
iris_df['label'] = iris.target
print(iris_df.head(10))
print("=" * 30)

#훈련 데이터 / 테스트 데이터 나누기
from sklearn.model_selection import train_test_split
X_train, X_test, y_train, y_test = train_test_split(iris_data,iris_label, test_size=0.2,random_state=11)
    

# KNN을 이용한 품종 분류 ===========================
from sklearn.neighbors import KNeighborsClassifier

knn = KNeighborsClassifier(n_neighbors=3) 

# KNN 분류기를 훈련셋으로 훈련시킵니다. 
knn.fit(X_train, y_train) 

# 테스트셋의 라벨값을 예측합니다. 
y_pred = knn.predict(X_test) 

print("예측 정확도: {0:.4f}".format(np.mean(y_pred == y_test)))
print("=" * 30)

# 새로운 품종 예측 
X_new = np.array([[5, 2.9, 1, 0.2]])
prdct = knn.predict(X_new)
print("예측값: {}, ".format(prdct), 
      "예측한 품종: {}".format(iris['target_names'][prdct]))
print("=" * 30)


# DecisionTreeClassifier를 이용한 품종 분류 ==========
from sklearn.tree import DecisionTreeClassifier

# DecisionTreeClassifier 객체 생성 
dt_clf = DecisionTreeClassifier(random_state=11)

# 학습 수행 
dt_clf.fit(X_train, y_train)

# 학습이 완료된 DecisionTreeClassifier 
# 객체에서 테스트 데이터 세트로 예측 수행. 
pred = dt_clf.predict(X_test)

# 정확도 측정
from sklearn.metrics import accuracy_score
print("예측 정확도: {0:.4f}".format(accuracy_score(y_test,pred)))
print("=" * 30)

# 새로운 품종 예측 
X_new = np.array([[5, 2.9, 1, 0.2]])
prdct = dt_clf.predict(X_new)
print("예측값: {}, ".format(prdct), "예측한 품종: {}".
      format(iris['target_names'][prdct]))
print("=" * 30)










