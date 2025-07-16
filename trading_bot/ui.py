import streamlit as st
import pandas as pd
from .self_learning import load_trades


def main():
    st.title("AI Trading Bot")
    trades = load_trades()
    st.subheader("Trade Log")
    st.dataframe(trades)


if __name__ == '__main__':
    main()
