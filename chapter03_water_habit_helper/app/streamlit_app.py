from pathlib import Path
import pandas as pd


ROOT = Path(__file__).resolve().parents[1]
SUGGESTION_PATH = ROOT / "outputs" / "suggestions.csv"


def cli_view():
    if not SUGGESTION_PATH.exists():
        print("请先运行 python run_demo.py 生成提醒建议。")
        return
    frame = pd.read_csv(SUGGESTION_PATH)
    print("\n饮水习惯助手（命令行预览）\n")
    print(frame.to_string(index=False))


try:
    import streamlit as st
except ImportError:
    if __name__ == "__main__":
        cli_view()
else:
    st.set_page_config(page_title="饮水习惯助手", layout="wide")
    st.title("饮水习惯助手")
    st.caption("用于课堂演示的高风险提醒预览界面。")
    if not SUGGESTION_PATH.exists():
        st.warning("请先运行 python run_demo.py。")
    else:
        frame = pd.read_csv(SUGGESTION_PATH)
        st.dataframe(frame, use_container_width=True)
