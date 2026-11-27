const api_url="http://localhost:5000/itens";
document.addEventListener("DOMContentLoaded", () => {
    carregaritens();
    document.getElementById("from-cadastro").addEventListener("submit", cadastraritem);
});
async function carregaritens() {
    try{
        const resposta = await fetch(api_url); 
        const itens = await resposta.json();
        const tabela = document.getElementById("tabela-itens");
        tabela.innerHTML = "";
        itens.forEach (item => {
        const tr = document.createElement("tr");
        const botaoacao = item.status === "disponivel"
        ? `<button onclick = "devolveritem(${item.id})">devolver</button>`
        : `<span>retirado por: <b>${item.retirado_por}</b></span>`;
        
        tr.innerHTML = `
        <td>${item.id}</td>
        <td>${item.titulo}</td>
        <td>${item.descricao || "-"}</td>
        <td>${item.local_encontrado}</td>
        <td>${item.data_encontro}</td>
        <td>${item.status}</td>
        <td>
        ${botaoacao}
        <button onclick = "deletaritem(${item.id})"
        style = "background:#b91c1c;">excluir</button>
        </td>
        `;
        tabela.appendChild(tr);
        });
    } catch (erro) {
        console.error("erro ao encontrar com a API do python:", erro);
    }
}
async function cadastraritem(evento){
evento.preventdefault();

const novoitem = {
    titulo: document.getElementById("titulo").value,
    descricao: document.getElementById("descricao").value,
    local_encontrado: document.getElementById("local_encontrado").value,
    data_encontro: document.getElementById("data_encontro").value
};
const resposta = await fetch(api_url, {
    method: "post",
    headers: {"content-type": "applcation/json"},
    body: JSON.stringify(novoitem)
});

if (resposta.ok){
    document.getElementById("from-cadrasto").reset();
    carregaritens();
} else {
    const erro = await resposta.json();
    alert("erro ao cadastrar:" + erro.erro);
 }
}

async function devolveritem(id) {
    const nomepessoa = prompt("digite o nome de quem esta retirando o item:");
    if (!nomepessoa) return; 
}
    
