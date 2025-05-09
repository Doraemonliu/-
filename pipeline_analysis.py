import pandas as pd
import matplotlib.pyplot as plt
from sklearn.linear_model import LogisticRegression
from sklearn.preprocessing import LabelEncoder

def load_and_preprocess_data(filepath):
    """
    加载并预处理CSV数据
    :param filepath: CSV文件路径
    :return: 预处理后的数据和标签
    """
    try:
        data = pd.read_csv(filepath, encoding='utf-8')
    except UnicodeDecodeError:
        try:
            data = pd.read_csv(filepath, encoding='gbk')
        except UnicodeDecodeError:
            data = pd.read_csv(filepath, encoding='utf-16')
    
    # 对分类变量进行编码
    le = LabelEncoder()
    if '组合方式' in data.columns:
        data['组合方式'] = le.fit_transform(data['组合方式'])
    
    # 验证数据维度并提取特征
    if len(data.columns) < 2:
        raise ValueError("数据至少需要两列（特征列和目标列）")
    
    # 确保有足够的特征列
    feature_cols = [col for col in data.columns if col != '组合方式']
    if len(feature_cols) < 1:
        raise ValueError("未找到有效的特征列")
    
    # 提取特征和目标变量
    X = data[feature_cols[:-1]] if len(feature_cols) > 1 else data[[feature_cols[0]]]
    y = data[feature_cols[-1]]
    
    return X, y

def train_model(X, y):
    """
    训练逻辑回归模型
    :param X: 特征数据
    :param y: 目标变量
    :return: 训练好的模型
    """
    model = LogisticRegression(max_iter=1000)
    model.fit(X, y)
    return model

def find_optimal_pipeline(model, X):
    """
    找出最优管道配置
    :param model: 训练好的模型
    :param X: 特征数据
    :return: 最优配置的索引和预测概率
    """
    probabilities = model.predict_proba(X)[:, 1]
    optimal_idx = probabilities.argmax()
    return optimal_idx, probabilities[optimal_idx]

def visualize_data(X, optimal_idx):
    """
    可视化数据分布并标注最优配置
    :param X: 特征数据
    :param optimal_idx: 最优配置索引
    """
    plt.figure(figsize=(10, 6))
    
    # 绘制所有数据点
    plt.scatter(X.index, X.iloc[:, 0], color='blue', alpha=0.5, label='普通配置')
    
    # 标注最优配置
    plt.scatter(optimal_idx, X.iloc[optimal_idx, 0], color='red', s=100, 
               label=f'最优配置 (索引: {optimal_idx})')
    
    plt.xlabel('配置索引')
    plt.ylabel('特征值')
    plt.title('管道配置分布与最优配置')
    plt.legend()
    plt.grid(True)
    plt.show()

if __name__ == "__main__":
    # 示例用法
    csv_path = "pipeline_data.csv"  # 替换为实际CSV文件路径
    
    try:
        X, y = load_and_preprocess_data(csv_path)
        model = train_model(X, y)
        optimal_idx, prob = find_optimal_pipeline(model, X)
        
        print(f"最优管道配置索引: {optimal_idx}")
        print(f"预测概率: {prob:.4f}")
        print("最优配置详情:")
        print(X.iloc[optimal_idx])
        
        # 调用可视化函数
        visualize_data(X, optimal_idx)
    except FileNotFoundError:
        print(f"错误: 文件 {csv_path} 未找到，请检查路径")
    except Exception as e:
        print(f"发生错误: {str(e)}")