from flask import Flask, request, jsonify
from flask_cors import CORS
from conexao import conectar

app = Flask(__name__)
CORS(app) #libera o acesso do frontend HTML/JS

#[R] READ - listar todos os itens cadastrados
@app.route("/itens", methods=["GET"])
def listar_itens():
    conn = conectar()
    cursor = conn.cursor(dictionary=True)

    cursor.execute("SELECT * from itens ORDER BY id DESC")
    lista = cursor.fetchall()

    cursor.close()
    conn.close()
    return jsonify(lista), 200

#[C] CREATE - cadastrar um novo item pedido 
@app.route("/itens", methods=["POST"])
def criar_itens():
    dados = request.get_json()
    if not dados.get("titulo") or not dados.get("local_encontrado"):
        return jsonify({"erro": "titulo e local sâo obrigatorios!"}), 400
    
    conn = conectar()
    cursor = conn.cursor()
    sql = """
    INSERT INTO itens (titulo, descricao, local_encontrado, data_encontro)
    VALUES (%s, %s, %s, %s)
    """
    valores = (
        dados["titulo"],
        dados.get("descricao",""),
        dados["local_encontrado"],
        dados["data_encontro"]
    )

    cursor.execute(sql, valores)
    conn.commit() #confirma a gravação no banco!

    novo_id = cursor.lastrowid
    cursor.close()
    conn.close()
    return jsonify({"mensagem": "item cadastrado!", "id": novo_id }), 201

#[U] UPDATE - resgistrar a devolução de um item pelo id
@app.route("/itens/<int:id>/devolver", methods=["PUT"])
def devolver_item(id):
    dados = request.get_json()
    retirado_por = dados.get("retirado_por")

    if not retirado_por:
        return jsonify({"erro": "Informe o nome de quem retirou o item."}), 400

    conn = conectar()
    cursor = conn.cursor()

    sql = """
        UPDATE itens
        SET status = 'Devolvido', retirado_por = %s
        WHERE id = %s
    """

    cursor.execute(sql, (retirado_por, id))
    conn.commit()

    linhas_afetadas = cursor.rowcount
    cursor.close()
    conn.close()

    if linhas_afetadas == 0:
        return jsonify({"erro": "Item não encontrado."}), 404

    return jsonify({"mensagem": "Devolução registrada com sucesso!"}), 200

@app.route("/itens/<int:id>", methods= ["DELETE"])
def deletar_item(id):
    conn = conectar()
    cursor = conn.cursor()

    sql = "DELETE FROM itens WHERE id = %s"
    cursor.execute(sql, (id,))
    conn.commit()

    linhas_afetadas = cursor.rowcount
    cursor.close()
    conn.close()

    if linhas_afetadas == 0:
        return jsonify({"erro": "Item não encontrado."}), 404
    
    return jsonify ({"mensagem:" "Item removido do sistema."}), 200

if __name__ == "__main__":
    app.run(debug=True, port= 5000)