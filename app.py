import streamlit as st
import numpy as np
from ca import evolve
import matplotlib.pyplot as plt
from rules import common_rules

def run_ca(state, rule, radius, size, steps, col2):
    st.session_state['history'].append(state)
    for _ in range(steps):
        state = evolve(state, rule, radius, size)
        st.session_state['history'].append(state)

    max_len = max([len(state) for state in st.session_state['history']])
    plot_image = []
    for state in st.session_state['history']:
        diff_from_max = max_len - len(state)
        if diff_from_max > 0:
            new_line = state + [0 for i in range(diff_from_max)]
            plot_image.append(new_line)
        else:
            plot_image.append(state)
    print("PLOT \n", plot_image)
    # plot_image = [st.session_state['history'][i] + [0] * (max_len - len(st.session_state['history'][i])) for i in range(len(st.session_state['history']))]
    im = plt.imshow(plot_image, aspect='auto', cmap='Greys')

    with col2:
        st.pyplot(im.get_figure())    

def clear_history():
    st.session_state['history']=[]

def show_len():
    print((st.session_state['history']))

st.set_page_config(layout="wide", initial_sidebar_state="expanded")


title_col, button_col  = st.columns([3, 1])
with title_col:
    st.title("Reprogammable Cellular Automata")

input_header_col, plot_header_col = st.columns([0.3, 0.5])
input_state_col, plot_col = st.columns([0.3, 0.7 ])

# Initialization
if 'history' not in st.session_state:
    st.session_state['history'] = []


# Sidebar contains all parameters to be set by the user
with st.sidebar:
    st.image("duth_logo.png", width=200)
    # Base User Parameters
    with st.container(border=True):
        
        st.header("Base Parameters")
        steps = int(st.number_input("Time steps to run:", step=1, min_value=0))
        states = int(st.number_input("Number of states:", step=1, min_value=2, max_value=36))
        size = int(st.number_input("Array Size:", step=1, min_value=5))
        radius = int(st.number_input("Radius length:", step=1, min_value=1, max_value=int(size/2)))

    # Show rules only after both states and radius are set
    if states > 0 and radius > 0:
        selection = st.selectbox(label="Common CA rules", options=common_rules, index=None)
        if selection is not None:
            selected_rule = common_rules[selection]
        else:
            selected_rule = None

        # Rules as checkboxes
        with st.expander(label="Create Custom Rule"):
            total_rules = (states) ** (radius*2+1)
            # st.header("Custom rule:")
            custom_rule = {}

            for i in range(total_rules):
                msg = str(np.base_repr(i, base=states)).zfill(radius*2+1)
                custom_rule[msg] = st.number_input(f"{msg}", step=1, min_value=0, max_value=states-1)

        if selected_rule is None:
            rule = custom_rule
        else:
            rule = selected_rule 

with input_header_col:
    st.header("Choose input state.")
    st.caption("Selected boxes are 1s, rest are 0s")

with input_state_col:
    if size > 0:
        initial_state = list(np.zeros(size, dtype=int))

        for i in range(size):
            initial_state[i] = st.selectbox(label=f"input_state_{i}", options=range(states))

with button_col:
    if 'initial_state' in locals():
        if not st.session_state['history']:
            state = initial_state
        else:
            state = st.session_state['history'][-1]

        st.button(
            "Run", 
            on_click=run_ca,
            type="primary",
            disabled=(steps<=0 or states<=0 or size<=0 or radius<=0),
            args=(state, rule, radius, size, steps, plot_col),
            use_container_width=True
        )

        st.button(
            "Clear History",
            type="primary",
            on_click=clear_history,
            use_container_width=True
        )