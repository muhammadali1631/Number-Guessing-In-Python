import streamlit as st
import random

# Set page configuration
st.set_page_config(
    page_title="Number Guessing Game",
    page_icon="🎮",
    layout="centered"
)

# Ensure all session state variables are initialized
if 'game_started' not in st.session_state:
    st.session_state.game_started = False
if 'random_number' not in st.session_state:
    st.session_state.random_number = None
if 'attempts' not in st.session_state:
    st.session_state.attempts = 0
if 'game_over' not in st.session_state:
    st.session_state.game_over = False
if 'message' not in st.session_state:
    st.session_state.message = ""
if 'min_range' not in st.session_state:
    st.session_state.min_range = 1
if 'max_range' not in st.session_state:
    st.session_state.max_range = 100
if 'selected_range' not in st.session_state:
    st.session_state.selected_range = "Easy (1-25)"  # Default difficulty

# Maximum attempts allowed
MAX_ATTEMPTS = 7

# Available difficulty levels and their number ranges
RANGES = {
    "Easy (1-25)": (1, 25),
    "Medium (1-50)": (1, 50),
    "Hard (1-75)": (1, 75),
    "Expert (1-100)": (1, 100)
}

# Function to start a new game
def start_game():
    range_name = st.session_state.selected_range  # Already initialized
    min_val, max_val = RANGES[range_name]
    st.session_state.min_range = min_val
    st.session_state.max_range = max_val
    st.session_state.random_number = random.randint(min_val, max_val)
    st.session_state.attempts = 0
    st.session_state.game_over = False
    st.session_state.message = ""
    st.session_state.game_started = True

# Function to reset the game
def reset_game():
    st.session_state.game_started = False
    st.session_state.random_number = None
    st.session_state.attempts = 0
    st.session_state.game_over = False
    st.session_state.message = ""

# App title
st.title("🎮 Number Guessing Game")

# Game setup or gameplay
if not st.session_state.game_started:
    st.markdown("### Game Setup")
    st.markdown("Choose your difficulty level and start the game!")
    
    # Difficulty selection
    selected_range = st.selectbox(
        "Select difficulty level:",
        options=list(RANGES.keys()),
        index=list(RANGES.keys()).index(st.session_state.selected_range)
    )
    
    # Store selected range in session state
    st.session_state.selected_range = selected_range
    
    # Centered start game button
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        if st.button("Start Game", use_container_width=True):
            start_game()
    
    with st.expander("How to Play"):
        st.markdown(f"""
        1. Select your difficulty level (determines the range of numbers).
        2. Click "Start Game" to begin.
        3. You have {MAX_ATTEMPTS} attempts to guess the correct number.
        4. Each guess gets a hint if it's too high or too low.
        5. Try to find the number before running out of attempts!
        """)

else:
    range_name = st.session_state.selected_range
    st.markdown(f"🎯 Try to guess the number between **{st.session_state.min_range}** and **{st.session_state.max_range}** in **{MAX_ATTEMPTS} attempts**!")
    st.markdown(f"**Difficulty Level:** {range_name}")
    
    col1, col2 = st.columns([3, 1])
    with col1:
        guess = st.number_input(
            "Enter your guess:", 
            min_value=st.session_state.min_range, 
            max_value=st.session_state.max_range, 
            step=1, 
            key="guess_input", 
            disabled=st.session_state.game_over
        )
    
    with col2:
        if st.button("Guess!", use_container_width=True, disabled=st.session_state.game_over):
            st.session_state.attempts += 1
            if guess < st.session_state.random_number:
                st.session_state.message = "🔼 Too low! Try a higher number."
            elif guess > st.session_state.random_number:
                st.session_state.message = "🔽 Too high! Try a lower number."
            else:
                st.session_state.message = f"🎉 Congratulations! You guessed the number in {st.session_state.attempts} attempts!"
                st.session_state.game_over = True
            if st.session_state.attempts >= MAX_ATTEMPTS and not st.session_state.game_over:
                st.session_state.message = f"❌ Game over! The correct number was **{st.session_state.random_number}**."
                st.session_state.game_over = True
    
    if st.session_state.message:
        if "Congratulations" in st.session_state.message:
            st.success(st.session_state.message)
        elif "Game over" in st.session_state.message:
            st.error(st.session_state.message)
        elif "low" in st.session_state.message:
            st.warning(st.session_state.message)
        elif "high" in st.session_state.message:
            st.info(st.session_state.message)
    
    if st.session_state.attempts > 0:
        st.markdown(f"**Attempts used:** {st.session_state.attempts}/{MAX_ATTEMPTS}")
        st.progress(st.session_state.attempts / MAX_ATTEMPTS)
    
    st.markdown("---")
    col1, col2, col3 = st.columns(3)
    with col1:
        if st.button("New Game", use_container_width=True):
            reset_game()
    with col2:
        if not st.session_state.game_over:
            if st.button("Show Hint", use_container_width=True):
                st.info("💡 Try guessing in the middle of your possible range to eliminate half the numbers each time.")
    with col3:
        if st.session_state.game_over:
            if st.button("Play Again", use_container_width=True):
                start_game()
    
    st.markdown("### 📊 Game Stats")
    col1, col2 = st.columns(2)
    with col1:
        st.markdown(f"**Number Range:** {st.session_state.min_range} - {st.session_state.max_range}")
        st.markdown(f"**Max Attempts:** {MAX_ATTEMPTS}")
    with col2:
        if st.session_state.attempts > 0 and not st.session_state.game_over:
            remaining_attempts = MAX_ATTEMPTS - st.session_state.attempts
            st.markdown(f"**Remaining Attempts:** {remaining_attempts}")
            if remaining_attempts <= 3:
                st.warning("⚠️ Running low on attempts!")
