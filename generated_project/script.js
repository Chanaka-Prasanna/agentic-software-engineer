// Game state variables
const gameBoard = ['', '', '', '', '', '', '', '', ''];
let currentPlayer = 'X';
let gameActive = true;

// Constants for player marks
const PLAYER_X = 'X';
const PLAYER_O = 'O';

// DOM element references
const gameBoardElement = document.querySelector('.game-board');
const cells = document.querySelectorAll('.cell');
const gameStatusElement = document.querySelector('.game-status');
const resetButton = document.querySelector('.reset-button');

// Function to update the game status message
const updateGameStatus = (message) => {
    gameStatusElement.textContent = message;
};

// Function to handle a cell click
const handleCellClick = (event) => {
    const clickedCell = event.target;
    const clickedCellIndex = parseInt(clickedCell.dataset.cellIndex);

    // If the cell is already occupied or the game is not active, do nothing
    if (gameBoard[clickedCellIndex] !== '' || !gameActive) {
        return;
    }

    // Update game state
    gameBoard[clickedCellIndex] = currentPlayer;
    clickedCell.textContent = currentPlayer;
    clickedCell.classList.add(currentPlayer.toLowerCase());

    // Check for win or draw
    if (checkWin()) {
        updateGameStatus(`${currentPlayer} has won!`);
        gameActive = false;
        return;
    }

    if (checkDraw()) {
        updateGameStatus('Game ended in a draw!');
        gameActive = false;
        return;
    }

    // Switch player
    currentPlayer = currentPlayer === PLAYER_X ? PLAYER_O : PLAYER_X;
    updateGameStatus(`It's ${currentPlayer}'s turn`);
};

// Function to check for a win
const checkWin = () => {
    const winningConditions = [
        [0, 1, 2],
        [3, 4, 5],
        [6, 7, 8],
        [0, 3, 6],
        [1, 4, 7],
        [2, 5, 8],
        [0, 4, 8],
        [2, 4, 6]
    ];

    for (let i = 0; i < winningConditions.length; i++) {
        const condition = winningConditions[i];
        const [a, b, c] = condition;

        if (gameBoard[a] === currentPlayer &&
            gameBoard[b] === currentPlayer &&
            gameBoard[c] === currentPlayer) {
            return true; // A win is detected
        }
    }
    return false; // No win detected
};

// Function to check for a draw
const checkDraw = () => {
    return gameBoard.every(cell => cell !== ''); // Check if all cells are filled
};

// Function to reset the game
const resetGame = () => {
    // Reset game state variables
    gameBoard.fill(''); // Reset gameBoard to an array of empty strings
    currentPlayer = PLAYER_X;
    gameActive = true;

    // Visually clear all cells and remove player classes
    cells.forEach(cell => {
        cell.textContent = '';
        cell.classList.remove(PLAYER_X.toLowerCase(), PLAYER_O.toLowerCase());
    });

    // Update the game status display
    updateGameStatus(`It's ${currentPlayer}'s turn`);

    // Re-attach event listeners to cells
    // First, remove any existing listeners to prevent duplicates
    cells.forEach(cell => {
        cell.removeEventListener('click', handleCellClick);
    });
    // Then, add them back
    cells.forEach(cell => {
        cell.addEventListener('click', handleCellClick);
    });

    // Re-attach event listener to the reset button
    // Remove any existing listener first
    resetButton.removeEventListener('click', resetGame);
    // Then, add it back
    resetButton.addEventListener('click', resetGame);
};

// Initialize the game by calling resetGame
resetGame();