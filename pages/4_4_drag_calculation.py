# 4_drag_calculation.py

import streamlit as st
import matplotlib.pyplot as plt


def main():

    def simple_plot():
        x = list(range(1, 11))  # Numbers 1 through 10
        y = x  # Same as x, so we get a straight line

        plt.plot(x, y)
        st.pyplot()
    
    simple_plot()

if __name__ == "__main__":
    main()
