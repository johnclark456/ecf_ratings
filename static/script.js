document.addEventListener('DOMContentLoaded', () => {
    const fetchBtn = document.getElementById('fetchBtn');
    const playerInput = document.getElementById('playerInput');
    const resultsSection = document.getElementById('resultsSection');
    const resultsTableBody = document.querySelector('#resultsTable tbody');
    const resultCount = document.getElementById('resultCount');

    fetchBtn.addEventListener('click', async () => {
        const text = playerInput.value;
        const names = text.split('\n').filter(n => n.trim().length > 0);

        if (names.length === 0) {
            alert('Please enter at least one player name.');
            return;
        }

        // UI State: Loading
        fetchBtn.classList.add('loading');
        fetchBtn.disabled = true;
        resultsSection.classList.add('hidden');
        resultsTableBody.innerHTML = '';

        try {
            const response = await fetch('/api/ratings', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify({ names: names })
            });

            const data = await response.json();

            if (data.results) {
                renderResults(data.results);
            } else if (data.error) {
                alert('Error: ' + data.error);
            }
        } catch (error) {
            console.error('Error fetching ratings:', error);
            alert('An error occurred while fetching ratings.');
        } finally {
            // UI State: Reset
            fetchBtn.classList.remove('loading');
            fetchBtn.disabled = false;
        }
    });

    function renderResults(results) {
        resultsTableBody.innerHTML = '';

        results.forEach(player => {
            const row = document.createElement('tr');

            const nameCell = document.createElement('td');
            nameCell.textContent = player.name;

            const ratingCell = document.createElement('td');
            ratingCell.textContent = player.rating;

            // Highlight high ratings (example logic)
            if (player.rating >= 2000) {
                ratingCell.style.color = '#e2b340'; // Gold
                ratingCell.style.fontWeight = 'bold';
            }

            row.appendChild(nameCell);
            row.appendChild(ratingCell);
            resultsTableBody.appendChild(row);
        });

        resultCount.textContent = `${results.length} found`;
        resultsSection.classList.remove('hidden');
    }
});
