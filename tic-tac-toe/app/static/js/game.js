document.addEventListener('DOMContentLoaded', () => {
    const boardCells = document.querySelectorAll('.board-cell');
    const config = window.gameConfig;
    let isMyTurn = (config.currentPlayer === 'X' && config.isPlayerX) || 
                  (config.currentPlayer === 'O' && config.isPlayerO);
    let gameStatus = config.gameStatus;

    // Function to update the game board
    function updateBoard(boardState) {
        boardCells.forEach((cell, index) => {
            cell.innerHTML = boardState[index] !== ' ' 
                ? `<span class="player-${boardState[index]}">${boardState[index]}</span>` 
                : '';
        });
    }

    // Function to handle cell click
    function handleCellClick(event) {
        if (gameStatus === 'completed' || !isMyTurn) return;

        const cell = event.target.closest('.board-cell');
        if (!cell || cell.children.length > 0) return;

        const position = parseInt(cell.dataset.position);

        fetch(`/game/${config.gameId}/move`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({ position }),
        })
        .then(response => response.json())
        .then(data => {
            if (data.error) {
                alert(data.error);
                return;
            }

            updateBoard(data.board);
            isMyTurn = (data.current_player === 'X' && config.isPlayerX) || 
                      (data.current_player === 'O' && config.isPlayerO);
            gameStatus = data.game_status;

            if (gameStatus === 'completed') {
                setTimeout(() => {
                    window.location.reload();
                }, 2000);
            }
        })
        .catch(error => {
            console.error('Error:', error);
            alert('An error occurred while making your move.');
        });
    }

    // Add click event listeners to cells
    boardCells.forEach(cell => {
        cell.addEventListener('click', handleCellClick);
    });

    // Function to check for game updates
    function checkGameUpdates() {
        if (gameStatus === 'completed') return;

        fetch(`/game/${config.gameId}`)
            .then(response => response.json())
            .then(data => {
                if (data.error) {
                    console.error(data.error);
                    return;
                }

                if (data.board !== document.querySelector('.board-container').textContent) {
                    updateBoard(data.board);
                    isMyTurn = (data.current_player === 'X' && config.isPlayerX) || 
                              (data.current_player === 'O' && config.isPlayerO);
                    gameStatus = data.game_status;

                    if (gameStatus === 'completed') {
                        setTimeout(() => {
                            window.location.reload();
                        }, 2000);
                    }
                }
            })
            .catch(error => {
                console.error('Error:', error);
            });
    }

    // Poll for game updates every 2 seconds
    if (!isMyTurn && gameStatus !== 'completed') {
        setInterval(checkGameUpdates, 2000);
    }
}); 