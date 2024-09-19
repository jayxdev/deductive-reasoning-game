import streamlit as st
import numpy as np
import random
import time

icons = ["🟢", "🟥", "💙", "➕", "⭐"]


def try_to_fill_cell(grid, i, j, available_icons):
    available_cells = available_icons - set(grid[i, :]) - set(grid[:, j])
    if available_cells:
        shape = np.random.choice(list(available_cells), 1)[0]  # Choose a random shape from the available ones
        return shape
   
def create_puzzle_grid(size):
    shapes = np.random.choice(icons, size, replace=False) # Randomly choose shapes for the row
    grid = np.empty((size, size), dtype=str)
    for i in range(size):
        available_icons = set(shapes)
        for j in range(size):
            shape = try_to_fill_cell(grid, i, j, available_icons)
            if shape is None:
                return create_puzzle_grid(size)
            grid[i, j] = shape
            available_icons.remove(shape)
    return grid, shapes

def remove_icons(grid):
    grid_size = len(grid)  # Assuming grid is a square matrix
    num_icons = grid_size * grid_size
    removed_positions = random.sample(range(num_icons), random.randint(int(num_icons/3), int(num_icons/2.5)))  # Remove 5-10 icons
    question_mark_pos = random.choice(removed_positions)
    ans=grid[question_mark_pos//grid_size][question_mark_pos%grid_size]
    for pos in removed_positions:
        row, col = divmod(pos, grid_size)
        if pos == question_mark_pos:
            grid[row][col] = "❔"  # Question mark
        else:
            grid[row][col] = "‎"  # Empty space
    
    return grid, question_mark_pos,ans

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

def game():
    # Generate the grid and modify it
    # Initialize session state
    st.session_state.current_puzzle, st.session_state.shapes = create_puzzle_grid(st.session_state.grid_size)
    st.session_state.puzzle_grid, st.session_state.question_mark_pos, st.session_state.ans = remove_icons(st.session_state.current_puzzle) 
    
    # Display the grid
    display_grid(st.session_state.puzzle_grid)
    
    # Show options for the user to click
    columns=st.columns(1)
    with columns[0]:
        st.write("#### Click on the shape that should replace the question mark:")  
    display_options()    
            
def display_options():
     # Display shape options as horizontal buttons
    columns = st.columns(len(st.session_state.shapes)+6)
    for i, shape in enumerate(st.session_state.shapes):
        with columns[i+3]:
            st.button(shape, key=f"shape_{i}", on_click=check_answer, args=(shape, st.session_state.ans))

def check_answer(selected_shape,ans):
    # Get the original shape
    message_placeholder = st.empty()
    if selected_shape == ans:
        message_placeholder.success("Congratulations! You correctly identified the shape.", icon="✅")
        st.session_state.score+=1
        st.session_state.max_score=max(st.session_state.score,st.session_state.max_score)
    else:
        message_placeholder.error(f"Oops! The correct shape was {ans}. Try again.")
        st.session_state.score=0
    time.sleep(1.5)
    message_placeholder.empty()    
    reset_game()    

def reset_game():          
    for key in st.session_state.keys():
        if key.startswith("button_") or key.startswith("shape_"):
            del st.session_state[key]
            
        

if __name__ == "__main__":
    st.set_page_config(
        page_title="Capgemini Puzzle Game",
        page_icon="🧩",  # Add a puzzle icon
        layout="centered",  # Center the content
    )
    st.title("Capgemini Puzzle Game")

    # game interface elements

    st.sidebar.title("Instructions")
    st.sidebar.info("""Welcome to the Capgemini Puzzle Game!
    Instructions: Choose a shape such that all shapes are disinct in that row and column.
    """)
    #grid sizes are 3x3, 4x4, 5x5
    if "Grid Size" not in st.session_state:
        st.session_state.grid_size=3
    st.session_state.grid_size = st.sidebar.slider("Grid Size", min_value=3, max_value=5, value=st.session_state.grid_size)
    if "score" not in st.session_state:
        st.session_state.score=0
        st.session_state.max_score=0
    if st.session_state.score>5:
        st.session_state.grid_size = 4
    if st.session_state.score > 10:
        st.session_state.grid_size = 5          
    st.sidebar.write(f"Score: {st.session_state.score}")
    st.sidebar.write(f"Max Score: {st.session_state.max_score}")
    game()

    