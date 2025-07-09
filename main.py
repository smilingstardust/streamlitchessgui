import streamlit as st
import chess
import chess.svg

# Initialize the board in session state
if 'board' not in st.session_state:
    st.session_state.board = chess.Board()

# Title
st.title("Interactive Chess GUI")

# Sidebar controls
st.sidebar.header("Controls")
move_input = st.sidebar.text_input("Enter your move (UCI or SAN)", value="")
if st.sidebar.button("Make Move"):
    try:
        # Try SAN first, then UCI
        try:
            move = st.session_state.board.parse_san(move_input)
        except ValueError:
            move = chess.Move.from_uci(move_input)
        if move in st.session_state.board.legal_moves:
            st.session_state.board.push(move)
        else:
            st.sidebar.error("Illegal move.")
    except Exception as e:
        st.sidebar.error(f"Invalid move: {e}")

if st.sidebar.button("Reset Game"):
    st.session_state.board.reset()

# Display current board
svg_board = chess.svg.board(board=st.session_state.board, size=400)
st.write(svg_board, unsafe_allow_html=True)

# Show turn and status
if st.session_state.board.is_checkmate():
    st.success(f"Checkmate! {'White' if st.session_state.board.turn == chess.BLACK else 'Black'} wins.")
elif st.session_state.board.is_stalemate():
    st.info("Stalemate.")
elif st.session_state.board.is_check():
    st.warning(f"Check to {'White' if st.session_state.board.turn == chess.WHITE else 'Black'}.")
else:
    st.write(f"Turn: {'White' if st.session_state.board.turn == chess.WHITE else 'Black'}")

# Move history
st.subheader("Move History")
st.text(st.session_state.board.move_stack)
