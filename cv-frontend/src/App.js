import React, { useState, useEffect } from 'react';
import './App.css';

function App() {
  const [adaylar, setAdaylar] = useState([]); 
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    fetch('http://127.0.0.1:8000/adaylar')
      .then(response => response.json())
      .then(data => {
        setAdaylar(data);
        setLoading(false);
      })
      .catch(error => {
        console.error('Hata:', error);
        setLoading(false);
      });
  }, []);

  return (
    <div className="App">
      <header className="App-header">
        <h1 style={{ color: '#61dafb' }}>İK Aday Analiz Paneli</h1>
        <p>Veritabanından Gelen Canlı Veriler</p>
        
        {loading ? (
          <p>Yükleniyor...</p>
        ) : (
          <table style={{ 
            width: '80%', 
            marginTop: '20px', 
            backgroundColor: '#282c34', 
            borderCollapse: 'collapse',
            fontSize: '18px'
          }} border="1">
            <thead>
              <tr style={{ backgroundColor: '#444' }}>
                <th>ID</th>
                <th>Aday İsmi</th>
                <th>Yetenekler</th>
                <th>Uyumluluk Puanı</th>
              </tr>
            </thead>
            <tbody>
              {adaylar.map(aday => (
                <tr key={aday.id} style={{ borderBottom: '1px solid #666' }}>
                  <td>{aday.id}</td>
                  <td>{aday.name}</td>
                  <td>{aday.skills}</td>
                  <td style={{ fontWeight: 'bold', color: aday.score > 70 ? '#4caf50' : '#ff9800' }}>
                    %{aday.score}
                  </td>
                </tr>
              ))}
            </tbody>
          </table>
        )}
      </header>
    </div>
  );
}

export default App;