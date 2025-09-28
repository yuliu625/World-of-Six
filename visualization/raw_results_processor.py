"""
从原始的数据日志中提取用于数据分析的结果。
需要额外处理文件树。
原始文件为：
    - game_context.json: context_controller记录的所有agent的响应。
    - game_history.json: game_history_controller记录的数值相关结果。需要进行统计推断分析。
结果为：
    与原本目录相同的结果，已整合多次实验。
"""

import pandas as pd

from pathlib import Path

import re
from typing import List


def clean_string(s):
    """
    清理字符串中的非法字符
    """
    if isinstance(s, str):
        # 移除所有不可见字符（除了换行符、制表符等常用字符）
        cleaned = re.sub(r'[^\x09\x0A\x0D\x20-\uD7FF\uE000-\uFFFD]', '', s)
        return cleaned
    return s


def clean_dataframe(df):
    """
    对数据框中的每个元素进行清理
    """
    return df.applymap(clean_string)


class RawResultsProcessor:
    def __init__(self, raw_results_dir, excel_results_dir):
        self.raw_results_dir = Path(raw_results_dir)
        self.excel_results_dir = Path(excel_results_dir)

    def run(self) -> None:
        for beta_dir in self.raw_results_dir.iterdir():
            for experiment_method_dir in beta_dir.iterdir():
                for price_method_dir in experiment_method_dir.iterdir():
                    results_dfs = []
                    for game_index_dir in price_method_dir.iterdir():
                        results_dfs.append(self.process_game_index_dir(game_index_dir))
                    dir_to_save = self.excel_results_dir / beta_dir.name / experiment_method_dir.name
                    dir_to_save.mkdir(exist_ok=True, parents=True)
                    result = self.concat_df(results_dfs)
                    # result = clean_dataframe(result)
                    self.save_df(result, dir_to_save / f"{price_method_dir.name}.xlsx")

    def process_game_index_dir(self, game_index_dir: Path) -> pd.DataFrame:
        df = self.get_experiment(game_index_dir)
        df['game_index'] = game_index_dir.name
        return df

    def get_experiment(self, experiment_dir: Path) -> pd.DataFrame:
        file_1_path = experiment_dir / 'game_context.json'
        file_2_path = experiment_dir / 'game_history.json'
        df1 = pd.read_json(file_1_path, lines=True)
        df2 = pd.read_json(file_2_path, lines=True)
        df_result = self.merge_df([df1, df2])
        return df_result

    def merge_df(self, df_list: List[pd.DataFrame]) -> pd.DataFrame:
        return pd.merge(*df_list, on=['game_round', 'participant_id', 'expectation'], how='inner')

    def concat_df(self, df_list: List[pd.DataFrame]) -> pd.DataFrame:
        return pd.concat(df_list, ignore_index=True)

    def read_json(self, path: Path) -> pd.DataFrame:
        return pd.read_json(path, lines=True)

    def save_df(self, df: pd.DataFrame, path: Path) -> None:
        df.to_excel(path, index=False)


if __name__ == '__main__':
    base_path = r"D:\document\code\paper\World-of-Six\results_qwen_turbo"
    raw_results_path = base_path + r"/results_raw"
    excel_results_path = base_path + r"/results_excel"
    raw_results_processor = RawResultsProcessor(raw_results_path, excel_results_path)
    raw_results_processor.run()
