const loadButton = document.querySelector('#loadButton');
const searchButton = document.querySelector('#searchButton');
const searchInput = document.querySelector('#searchInput');
const result = document.querySelector('#result');
const status = document.querySelector('#status');

function showCocktails(cocktails) {
    result.innerHTML = `
        <table>
            <thead>
                <tr>
                    <th>Название</th>
                    <th>Основа</th>
                    <th>Ингредиенты</th>
                    <th>Приготовление</th>
                    <th>Цена</th>
                </tr>
            </thead>
            <tbody>
                ${cocktails.map((cocktail, index) => `
                    <tr style="animation-delay: ${index * 45}ms">
                        <td>${cocktail.name}</td>
                        <td>${cocktail.base}</td>
                        <td>${cocktail.ingredients}</td>
                        <td>${cocktail.preparation}</td>
                        <td>${cocktail.price ? `${cocktail.price.toLocaleString('ru-RU')} ₽` : '—'}</td>
                    </tr>
                `).join('')}
            </tbody>
        </table>
    `;
}

async function requestData(url) {
    const response = await fetch(url);
    if (!response.ok) {
        const error = await response.json().catch(() => ({}));
        throw new Error(error.error || 'Ошибка сервера');
    }
    return response.json();
}

loadButton.addEventListener('click', async () => {
    loadButton.disabled = true;
    status.textContent = 'Загружаем барную карту из базы данных...';
    try {
        const cocktails = await requestData('/api/cocktails');
        showCocktails(cocktails);
        status.textContent = `В барной карте: ${cocktails.length} коктейлей`;
    } catch (error) {
        status.textContent = error.message;
    } finally {
        loadButton.disabled = false;
    }
});

searchButton.addEventListener('click', async () => {
    const query = searchInput.value.trim();
    if (!query) {
        status.textContent = 'Введите название коктейля или алкогольную основу';
        return;
    }
    searchButton.disabled = true;
    status.textContent = 'Ищем через специализированный web-сервис...';
    try {
        const cocktails = await requestData(`/api/search?query=${encodeURIComponent(query)}`);
        showCocktails(cocktails);
        status.textContent = `Найдено коктейлей: ${cocktails.length}`;
    } catch (error) {
        status.textContent = error.message;
    } finally {
        searchButton.disabled = false;
    }
});

searchInput.addEventListener('keydown', (event) => {
    if (event.key === 'Enter') {
        searchButton.click();
    }
});
