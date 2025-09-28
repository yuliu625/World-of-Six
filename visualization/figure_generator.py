import pandas as pd

import seaborn as sns
import matplotlib.pyplot as plt

from pathlib import Path


class FigureGenerator:
    def __init__(self, excel_results_path, figures_results_path):
        self.excel_results_dir = Path(excel_results_path)
        self.figures_results_dir = Path(figures_results_path)
        # self.figures_results_dir.relative_to(excel_results_path)

    def process_dir(self):
        ...

    def iter_results(self):
        for beta_dir in self.excel_results_dir.iterdir():
            # 获取当前beta的情况
            beta_name = beta_dir.name
            # 获取路径
            excel_no_history_no_guidance_dir = self.excel_results_dir / beta_name / "no_history_no_guidance"
            excel_no_guidance_dir = self.excel_results_dir / beta_name / "no_guidance"
            figures_no_history_no_guidance_dir = self.figures_results_dir / beta_name / "no_history_no_guidance"
            figures_no_guidance_dir = self.figures_results_dir / beta_name / "no_guidance"
            # 创建路径
            figures_no_history_no_guidance_dir.mkdir(exist_ok=True, parents=True)
            figures_no_guidance_dir.mkdir(exist_ok=True, parents=True)
            # 分别处理结果
            self.handle_no_history_results(excel_no_history_no_guidance_dir)
            self.handle_no_guidance_results(excel_no_guidance_dir)

    def handle_no_guidance_results(self, excel_no_guidance_dir):
        sequence_price_df_path = excel_no_guidance_dir / 'sequence_price.xlsx'
        reverse_price_df_path = excel_no_guidance_dir / 'reverse_price.xlsx'
        random_price_df_path = excel_no_guidance_dir / 'random_price.xlsx'
        same_price_dfs_path = [
            excel_no_guidance_dir / f'same_price_{i}.xlsx'
            for i in range(6)
        ]
        self.generate_prices_list_figures(sequence_price_df_path)
        self.generate_prices_list_figures(reverse_price_df_path)
        self.generate_prices_list_figures(random_price_df_path)
        [
            self.generate_same_price_figures(same_price_dfs_path[price_index])
            for price_index in range(6)
        ]

    def handle_no_history_results(self, no_history_dir):
        beta_name = no_history_dir.parent.name
        path_to_save = self.figures_results_dir / beta_name / 'no_history_no_guidance' / 'no_history_no_guidance.png'
        price_dfs = [
            pd.read_excel(no_history_dir / f'price_{i}.xlsx')
            for i in range(6)
        ]
        self.generate_no_history_figures(price_dfs, beta_name, path_to_save,)

    def generate_prices_list_figures(self, df_path: Path):
        df_name = df_path.stem
        experiment_method_name = df_path.parent.stem
        beta_name = df_path.parent.parent.stem
        path_to_save = self.figures_results_dir / beta_name / experiment_method_name / f"{df_name}.png"
        df = pd.read_excel(df_path)
        df = self.process_df(df, beta_name)
        # 设置图像风格
        sns.set(style="whitegrid")
        fig, ax = plt.subplots(figsize=(10, 6))
        sns.boxplot(
            ax=ax,
            data=df, x='t_price', y='expectation',
            color='lightblue', width=0.5,
            order=(
                ['2.24', '2.99', '3.74', '4.49', '5.24', '5.99']
                if beta_name == 'beta_025' else ['4.74', '4.99', '5.24', '5.49', '5.74', '5.99']
            ),
            fliersize=0.3
        )
        sns.lineplot(
            ax=ax,
            data=df, x='t_price', y='group_mean',
            label='mean of experiment results',
        )
        sns.lineplot(
            ax=ax,
            data=df, x='t_price', y='theoretical_solution',
            marker='o', linestyle='--', color='red',
            label='theoretical solution under FEE',
        )

        plt.ylim(-0.5, 6.5)
        ax.set_xlabel("price")
        ax.set_ylabel("expected number of buyers")
        plt.legend(loc='lower left')
        plt.savefig(path_to_save, dpi=300)

    def generate_same_price_figures(self, df_path: Path):
        price_index = df_path.stem[-1]
        experiment_method_name = df_path.parent.name
        beta_name = df_path.parent.parent.stem
        path_to_save = self.figures_results_dir / beta_name / experiment_method_name / f"same_price_{price_index}.png"
        df = pd.read_excel(df_path)
        df['group_mean'] = df.groupby('game_round')['expectation'].transform('mean')
        df['t_game_round'] = df['game_round'].astype(str)
        # 设置图像风格
        sns.set(style="whitegrid")

        # 绘制箱线图
        plt.figure(figsize=(10, 6))
        fig, ax = plt.subplots(figsize=(10, 6))
        sns.boxplot(
            ax=ax,
            data=df, x='t_game_round', y='expectation',
            color='lightblue', width=0.5,
            fliersize=0.3
        )
        sns.lineplot(
            ax=ax,
            data=df, x='t_game_round', y='group_mean',
            label='mean of experiment results',
        )
        sns.lineplot(
            ax=ax,
            data={
                't_game_round': ['1', '2', '3', '4', '5', '6', ],
                'expectation': [6-int(price_index) for _ in range(6)],
            }, x='t_game_round', y='expectation',
            marker='o', linestyle='--', color='red',
            label='theoretical solution under FEE',
        )
        # 添加标题和标签
        plt.ylim(-0.5, 6.5)
        ax.set_xlabel("game round")
        ax.set_ylabel("expected number of buyers")
        plt.legend(loc='lower left')
        plt.savefig(path_to_save, dpi=300)

    def generate_no_history_figures(self, df_list, beta_name,  path_to_save):
        df = pd.concat(df_list, ignore_index=True)
        df = self.process_df(df, beta_name)
        # 设置图像风格
        sns.set(style="whitegrid")
        # 绘制箱线图
        fig, ax = plt.subplots(figsize=(10, 6))
        sns.boxplot(
            ax=ax,
            data=df, x='t_price', y='expectation',
            order=(
                ['2.24', '2.99', '3.74', '4.49', '5.24', '5.99']
                if beta_name == 'beta_025' else ['4.74', '4.99', '5.24', '5.49', '5.74', '5.99']
            ),
            color='lightblue', width=0.5,
            fliersize=0.3
        )
        sns.lineplot(
            ax=ax,
            data=df, x='t_price', y='group_mean',
            label='mean of experiment results',
        )
        sns.lineplot(
            ax=ax,
            data=df, x='t_price', y='theoretical_solution',
            marker='o', linestyle='--', color='red',
            label='theoretical solution under FEE',
        )

        plt.ylim(-0.5, 6.5)
        ax.set_xlabel("price")
        ax.set_ylabel("expected number of buyers")
        plt.legend(loc='lower left')
        plt.savefig(path_to_save, dpi=300)

    def process_df(self, df, beta_name):
        theoretical_solution_map = None
        if beta_name == 'beta_025':
            theoretical_solution_map = {
                2.24: 6, 2.99: 5, 3.74: 4, 4.49: 3, 5.24: 2, 5.99: 1,
            }
        elif beta_name == 'beta_075':
            theoretical_solution_map = {
                4.74: 6, 4.99: 5, 5.24: 4, 5.49: 3, 5.74: 2, 5.99: 1,
            }
        df['theoretical_solution'] = df['price'].map(theoretical_solution_map)
        df['group_mean'] = df.groupby('price')['expectation'].transform('mean')
        df['t_price'] = df['price'].astype(str)
        return df

    def save_plot(self, path_to_save):
        plt.savefig(path_to_save)


if __name__ == '__main__':
    base_path = r"D:\document\code\paper\World-of-Six/results\results_qwen_turbo"
    excel_results = base_path + r"/results_excel"
    figure_results = base_path + r"/results_figures"

    figure_generator = FigureGenerator(excel_results, figure_results)
    figure_generator.iter_results()
