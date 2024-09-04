import streamlit as st
import numpy as np
import random

icons = ["🟢", "🟥", "💙", "➕", "⭐"]

def create_puzzle_grid(size):
    shapes = np.random.choice(icons, size, replace=False)
    grid = np.empty((size, size), dtype=str)
    for i in range(size):
        available_icons = set(shapes)
        for j in range(size):
            shape = try_to_fill_cell(grid, i, j, available_icons)
            grid[i, j] = shape
            available_icons.remove(shape)
    return grid

def try_to_fill_cell(grid, i, j, available_icons):
    available_cells = available_icons - set(grid[i, :]) - set(grid[:, j])
    if available_cells:
        shape = np.random.choice(list(available_cells), 1)[0]
        return shape
    else:
        try_to_fill_cell(grid, i, j, available_icons)

def display_grid(grid):
    # Display the grid
    columns = st.columns(3)
    #grid
    with columns[1]:
        for j,row in enumerate(grid):
            row_columns = st.columns(len(row))
            for i, shape in enumerate(row):
                with row_columns[i]:
                    if shape == "‎":
                        st.markdown(
                           """
                    <style>
                    .empty-cell {
                        height: 39.99px; /* Adjust height to match button */
                        width: 47.92px;  /* Adjust width to match button */
                        background-color: transparent;
                        border: 1px solid #ccc;  /* Add border */
                        border-radius: 8px;  /* Add rounded corners */
                        display: flex;
                        align-items: center;
                        justify-content: center;
                    }
                    </style>
                    <button class="empty-cell"></button>
                    """,
                            unsafe_allow_html=True
                        )
                    else:    
                        st.button(shape, key=f"button_{j}{i}")

grid = create_puzzle_grid(4)
display_grid(grid)
