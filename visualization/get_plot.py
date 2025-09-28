import seaborn as sns
import matplotlib.pyplot as plt

import pandas as pd


def get_plot(df_path: str, path_to_save: str):
    df = pd.read_excel(df_path, sheet_name='Sheet1')
    # 设置图像风格
    sns.set(style="whitegrid")

    # 绘制箱线图
    plt.figure(figsize=(10, 6))
    sns.boxplot(x='price', y='expectation', data=df, showmeans=True)

    # 添加标题和标签
    plt.title("Boxplot of expectation by price")
    plt.xlabel("price")
    plt.ylabel("expectation")

    # plt.show()
    plt.savefig(path_to_save, dpi=300)


if __name__ == '__main__':
    base_df_path = r""
    base_path_to_save = r""
    get_plot(
        r'D:\document\code\paper\World-of-Six\results_excel\qwen_15\network_effect_2_no_guidance_sequence_price.xlsx',
        r'D:\document\code\paper\World-of-Six\assets\figures\qwen_15/network_effect_2_no_guidance_sequence_price.png'
    )
