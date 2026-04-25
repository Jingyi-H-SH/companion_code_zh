from pathlib import Path
import pandas as pd

ROOT = Path(__file__).resolve().parents[1]
RISK_PATH = ROOT / "outputs" / "risk_predictions.csv"
SUGGESTION_PATH = ROOT / "outputs" / "suggestions.csv"


def cli_view():
    if not SUGGESTION_PATH.exists():
        print("请先运行 python run_demo.py。")
        return
    print("\n饮水习惯助手（命令行预览）\n")
    print(pd.read_csv(SUGGESTION_PATH).to_string(index=False))


try:
    import streamlit as st
except ImportError:
    if __name__ == "__main__":
        cli_view()
else:
    st.set_page_config(page_title="饮水习惯助手", layout="wide")
    st.title("饮水习惯助手")
    st.caption("用于查看饮水风险预测和生成提醒的读者版界面。")
    if not RISK_PATH.exists():
        st.warning("请先运行 python run_demo.py。")
    else:
        st.subheader("风险预测")
        st.dataframe(pd.read_csv(RISK_PATH), use_container_width=True)
        st.subheader("提醒建议")
        st.dataframe(pd.read_csv(SUGGESTION_PATH), use_container_width=True)
