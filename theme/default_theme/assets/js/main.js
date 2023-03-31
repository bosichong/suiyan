// JavaScript
const blog_url = suiyan.url
const searchInput = document.getElementById('search-input');
const searchBtn = document.getElementById('search-btn');
const modal = document.getElementById('modal');
const resultList = document.getElementById('result-list');

// 读取JSON文件
fetch(blog_url+'blog_data.json')
  .then(response => response.json())
  .then(data => {
    // 处理搜索按钮点击事件
    searchBtn.addEventListener('click', () => {
      const keyword = searchInput.value.trim().toLowerCase();
      const filteredArticles = data.filter(article => {
        return article.title.toLowerCase().includes(keyword);
      });
      // 清空搜索结果列表
      resultList.innerHTML = '';
      // 添加搜索结果到列表中
      if (filteredArticles.length === 0) {
        const li = document.createElement('li');
        li.textContent = '没有搜到相关内容';
        resultList.appendChild(li);
        modal.style.display = 'block';
      } else {
        filteredArticles.forEach(article => {
          const li = document.createElement('li');
          const a = document.createElement('a');
          a.href = blog_url+article.url+".html";
          a.target = '_blank';
          a.textContent = article.title;
          li.appendChild(a);
          resultList.appendChild(li);
        });
        modal.style.display = 'block';
      }
    });
  });
