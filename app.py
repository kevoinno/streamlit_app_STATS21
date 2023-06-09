import streamlit as st
import pandas as pd
from matplotlib import pyplot as plt
import io

st.sidebar.write("Exploratory Data Analysis")

uploaded_file = st.sidebar.file_uploader("Choose a file")

if uploaded_file is not None:
  # Can be used wherever a "file-like" object is accepted:
  df = pd.read_csv(uploaded_file)
  
  st.write(f'Dataframe has shape {df.shape}')

  show_dtypes = st.checkbox("Show data types of each column", key="disabled3", value = True)
  if show_dtypes:
    st.write(df.dtypes.rename("Data Types"))

  show_df = st.checkbox("Show Data Frame", key="disabled")

  if show_df:
    st.write(df)

  column_type = st.sidebar.selectbox('Select Data Type',
                                      ("Numerical", "Categorical/Boolean", "Date"))

  if column_type == "Numerical":
    numerical_column = st.sidebar.selectbox(
        'Select a Column', df.select_dtypes(include=['int64', 'float64']).columns)
    # summary statistics
    show_summary = st.checkbox("Show Summary Statistics", key = "disabled2", value = True)

    if show_summary:
      st.write(df[numerical_column].describe())
    # histogram
    choose_color = st.color_picker('Pick a Color', "#69b3a2")
    choose_opacity = st.slider(
        'Color Opacity', min_value=0.0, max_value=1.0, step=0.05, value = 1.0)

    hist_bins = st.slider('Number of bins', min_value=5,
                          max_value=150, value=30)
    hist_title = st.text_input('Set Title', 'Histogram')
    hist_xtitle = st.text_input('Set x-axis Title', numerical_column)

    fig, ax = plt.subplots()
    ax.hist(df[numerical_column], bins=hist_bins,
            edgecolor="black", color=choose_color, alpha=choose_opacity)
    ax.set_title(hist_title)
    ax.set_xlabel(hist_xtitle)
    ax.set_ylabel('Count')

    st.pyplot(fig)
    filename = "plot.png"
    fig.savefig(filename,dpi = 300)

    download_file_name = st.text_input('Set File Name For Download', 'plot')
    # Display the download button
    with open("plot.png", "rb") as file:
      btn = st.download_button(
          label="Download image",
          data=file,
          file_name=f"{download_file_name}.png",
          mime="image/png"
      )
  # barplots (categorical)
  elif column_type == "Categorical/Boolean":
      categorical_column = st.sidebar.selectbox('Select a Column', df.select_dtypes(include=['object']).columns)
      #proportions
      show_prop = st.checkbox(f"Show Categorical Proportions of {categorical_column}", key = "disabled4", value = True)
      if show_prop:
        st.write(df[categorical_column].value_counts() / len(df))
      choose_color = st.color_picker('Pick a Color', "#69b3a2")
      choose_opacity = st.slider(
        'Color Opacity', min_value=0.0, max_value=1.0, step=0.05, value = 1.0)
      fig, ax = plt.subplots()
      ax.bar(x = df[categorical_column].value_counts().index, height = df[categorical_column].value_counts(), color=choose_color, alpha=choose_opacity, edgecolor = "black")
      bar_title = st.text_input('Set Title', 'Barplot')
      bar_xtitle = st.text_input('Set x-axis Title', categorical_column)
      ax.set_title(bar_title)
      ax.set_xlabel(bar_xtitle)
      ax.set_ylabel('Count')
      st.pyplot(fig)
      filename = "plot.png"
      fig.savefig(filename,dpi = 300)

      download_file_name = st.text_input('Set File Name For Download', 'plot')
      #display download button
      with open("plot.png", "rb") as file:
        btn = st.download_button(
          label="Download image",
          data=file,
          file_name=f"{download_file_name}.png",
          mime="image/png"
      )