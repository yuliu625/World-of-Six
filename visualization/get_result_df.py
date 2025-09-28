import pandas as pd

from pathlib import Path


class ResultProcessor:
    def __init__(self, root_dir: str, folder_name: str, file_name1: str = 'game_history.json', file_name2: str = 'game_context.json'):
        self.root_dir = Path(root_dir)
        self.folder_name = folder_name
        self.file_name1 = file_name1
        self.file_name2 = file_name2

        self.file_path_list = self._get_file_path_list()
        self.df_list = self._get_df_list()
        self.result_df = self._concat_files()
        print(self.result_df)

    def _get_file_path_list(self):
        result = []
        for price_folder in self.root_dir.iterdir():
            if price_folder.name == self.folder_name:
                for experiment_folder in price_folder.iterdir():
                    file1_path = self.root_dir / price_folder / experiment_folder / self.file_name1
                    file2_path = self.root_dir / price_folder / experiment_folder / self.file_name2
                    result.append((file1_path, file2_path))
        return result

    def read_files(self, file_path):
        return pd.read_json(file_path, lines=True)

    def _get_df_list(self):
        return [
            self._merge_df(self.read_files(file_path1), self.read_files(file_path2))
            for file_path1, file_path2 in self.file_path_list
        ]

    def _merge_df(self, df1, df2):
        return pd.merge(df1, df2, on=['game_round', 'participant_id', 'expectation'], how='inner')

    def _concat_files(self):
        return pd.concat(self.df_list, ignore_index=True)

    def save_result(self, path_to_save: str):
        self.result_df.to_excel(path_to_save, index=False)


if __name__ == '__main__':
    result_processor = ResultProcessor(
        r'D:\document\code\paper\World-of-Six\results\no_guidance\network_effect_2',
        'reverse_order_price'
    )
    result_processor.save_result(
        r"D:\document\code\paper\World-of-Six\results_excel\qwen_15/network_effect_2_no_guidance_reverse_order.xlsx"
    )
