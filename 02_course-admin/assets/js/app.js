document.getElementById('searchButton')?.addEventListener('click', function () {

    const keyword =
        document.getElementById('keyword')?.value ?? '';

    alert(`검색어: ${keyword}`);
});