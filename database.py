import psycopg2

def get_connection():
    return psycopg2.connect(
        host="dpg-d506nvdactks73fgqee0-a.oregon-postgres.render.com",
        database="fullbelly_db",
        user="fullbelly_user",
        password="LGjXX7iBWNDkrxHHTiN0adYc1j7AWi1Z",
        port=5432,
        sslmode="require"
    )

def create_tables():
    conn = get_connection()
    cur = conn.cursor()

    # =======================
    # TABELA USUARIOS
    # =======================
    cur.execute("""
    CREATE TABLE IF NOT EXISTS usuarios (
        id SERIAL PRIMARY KEY,
        email VARCHAR(255) UNIQUE NOT NULL,
        nome VARCHAR(255) NOT NULL,
        documento VARCHAR(20) NOT NULL,
        telefone VARCHAR(20) NOT NULL,
        data_nascimento DATE,
        genero VARCHAR(20),
        endereco TEXT NOT NULL,
        senha_hash VARCHAR(255) NOT NULL,
        tipo VARCHAR(20) NOT NULL CHECK (tipo IN ('restaurante','beneficiario','voluntario')),
        descricao TEXT,
        aceita_newsletter BOOLEAN DEFAULT FALSE,
        status VARCHAR(20) DEFAULT 'ativo' CHECK (status IN ('ativo','inativo','pendente','suspenso')),
        foto_url VARCHAR(500),
        latitude DECIMAL(10,8),
        longitude DECIMAL(11,8),
        data_cadastro TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
        data_atualizacao TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
    );
    """)
    cur.execute("CREATE INDEX IF NOT EXISTS idx_usuario_tipo ON usuarios(tipo);")
    cur.execute("CREATE INDEX IF NOT EXISTS idx_usuario_status ON usuarios(status);")
    cur.execute("CREATE INDEX IF NOT EXISTS idx_usuario_email ON usuarios(email);")

    # =======================
    # TABELA RESTAURANTES
    # =======================
    cur.execute("""
    CREATE TABLE IF NOT EXISTS restaurantes (
        id SERIAL PRIMARY KEY,
        usuario_id INTEGER UNIQUE NOT NULL REFERENCES usuarios(id) ON DELETE CASCADE,
        tipo_estabelecimento VARCHAR(100),
        especialidade VARCHAR(255),
        horario_funcionamento VARCHAR(100),
        capacidade_doacao VARCHAR(20) CHECK (capacidade_doacao IN ('pequena','media','grande')),
        tipos_alimentos TEXT[] DEFAULT '{}',
        doacoes_realizadas INTEGER DEFAULT 0,
        avaliacao_media DECIMAL(3,2) DEFAULT 5.00,
        total_avaliacoes INTEGER DEFAULT 0,
        possui_certificado_doacao BOOLEAN DEFAULT FALSE,
        certificado_valido_ate DATE,
        data_criacao TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
        data_atualizacao TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
    );
    """)
    cur.execute("CREATE INDEX IF NOT EXISTS idx_restaurante_usuario ON restaurantes(usuario_id);")
    cur.execute("CREATE INDEX IF NOT EXISTS idx_restaurante_avaliacao ON restaurantes(avaliacao_media);")

    # =======================
    # TABELA BENEFICIARIOS
    # =======================
    cur.execute("""
    CREATE TABLE IF NOT EXISTS beneficiarios (
        id SERIAL PRIMARY KEY,
        usuario_id INTEGER UNIQUE NOT NULL REFERENCES usuarios(id) ON DELETE CASCADE,
        pessoas_familia INTEGER NOT NULL CHECK (pessoas_familia>0),
        criancas INTEGER DEFAULT 0 CHECK (criancas>=0),
        idosos INTEGER DEFAULT 0 CHECK (idosos>=0),
        renda_familiar VARCHAR(20) NOT NULL CHECK (renda_familiar IN ('ate-1','1-2','2-3','acima-3','sem-renda')),
        necessidades_especiais TEXT[] DEFAULT '{}',
        descricao_situacao TEXT,
        possui_deficiencia BOOLEAN DEFAULT FALSE,
        tipo_deficiencia VARCHAR(100),
        doacoes_recebidas INTEGER DEFAULT 0,
        ultima_doacao DATE,
        data_criacao TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
        data_atualizacao TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
    );
    """)
    cur.execute("CREATE INDEX IF NOT EXISTS idx_beneficiario_usuario ON beneficiarios(usuario_id);")

    # =======================
    # TABELA VOLUNTARIOS
    # =======================
    cur.execute("""
    CREATE TABLE IF NOT EXISTS voluntarios (
        id SERIAL PRIMARY KEY,
        usuario_id INTEGER UNIQUE NOT NULL REFERENCES usuarios(id) ON DELETE CASCADE,
        veiculo VARCHAR(20) NOT NULL CHECK (veiculo IN ('carro','moto','bicicleta','pe')),
        dias_disponiveis TEXT[] NOT NULL DEFAULT '{}',
        horario_preferido VARCHAR(20) CHECK (horario_preferido IN ('manha','tarde','noite','madrugada','qualquer')),
        raio_atuacao INTEGER DEFAULT 10 CHECK (raio_atuacao BETWEEN 1 AND 100),
        habilidades TEXT[] DEFAULT '{}',
        experiencia TEXT,
        status VARCHAR(20) DEFAULT 'disponivel' CHECK (status IN ('disponivel','em-missao','indisponivel','ferias')),
        disponivel_ate TIMESTAMP WITH TIME ZONE,
        missoes_completadas INTEGER DEFAULT 0,
        pontos INTEGER DEFAULT 0,
        avaliacao_media DECIMAL(3,2) DEFAULT 5.00,
        total_avaliacoes INTEGER DEFAULT 0,
        possui_cnh BOOLEAN DEFAULT FALSE,
        tipo_cnh VARCHAR(2),
        data_criacao TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
        data_atualizacao TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
    );
    """)
    cur.execute("CREATE INDEX IF NOT EXISTS idx_voluntario_usuario ON voluntarios(usuario_id);")
    cur.execute("CREATE INDEX IF NOT EXISTS idx_voluntario_status ON voluntarios(status);")
    cur.execute("CREATE INDEX IF NOT EXISTS idx_voluntario_disponibilidade ON voluntarios(status, disponivel_ate);")

    # =======================
    # TABELA DOACOES
    # =======================
    cur.execute("""
    CREATE TABLE IF NOT EXISTS doacoes (
        id SERIAL PRIMARY KEY,
        titulo VARCHAR(255) NOT NULL,
        descricao TEXT,
        tipo_alimento VARCHAR(100) NOT NULL,
        quantidade VARCHAR(100) NOT NULL,
        data_validade DATE,
        condicoes_armazenamento TEXT,
        temperatura_recomendada VARCHAR(50),
        contem_alergenicos BOOLEAN DEFAULT FALSE,
        alergenicos TEXT[] DEFAULT '{}',
        restricoes_dieta TEXT[] DEFAULT '{}',
        endereco_retirada TEXT NOT NULL,
        latitude DECIMAL(10,8),
        longitude DECIMAL(11,8),
        instrucoes_retirada TEXT,
        restaurante_id INTEGER NOT NULL REFERENCES usuarios(id) ON DELETE CASCADE,
        voluntario_id INTEGER REFERENCES usuarios(id) ON DELETE SET NULL,
        beneficiario_id INTEGER REFERENCES usuarios(id) ON DELETE SET NULL,
        status VARCHAR(20) DEFAULT 'disponivel' CHECK (status IN ('disponivel','reservado','retirado','entregue','cancelado','expirado')),
        motivo_cancelamento TEXT,
        data_criacao TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
        data_reserva TIMESTAMP WITH TIME ZONE,
        data_retirada TIMESTAMP WITH TIME ZONE,
        data_entrega TIMESTAMP WITH TIME ZONE,
        data_expiracao TIMESTAMP WITH TIME ZONE
    );
    """)
    cur.execute("CREATE INDEX IF NOT EXISTS idx_doacao_status ON doacoes(status);")
    cur.execute("CREATE INDEX IF NOT EXISTS idx_doacao_restaurante ON doacoes(restaurante_id);")
    cur.execute("CREATE INDEX IF NOT EXISTS idx_doacao_voluntario ON doacoes(voluntario_id);")
    cur.execute("CREATE INDEX IF NOT EXISTS idx_doacao_beneficiario ON doacoes(beneficiario_id);")
    cur.execute("CREATE INDEX IF NOT EXISTS idx_doacao_data_validade ON doacoes(data_validade);")
    cur.execute("CREATE INDEX IF NOT EXISTS idx_doacao_localizacao ON doacoes(latitude, longitude);")

    # =======================
    # TABELA MISSOES
    # =======================
    cur.execute("""
    CREATE TABLE IF NOT EXISTS missoes (
        id SERIAL PRIMARY KEY,
        voluntario_id INTEGER NOT NULL REFERENCES usuarios(id) ON DELETE CASCADE,
        doacao_id INTEGER NOT NULL REFERENCES doacoes(id) ON DELETE CASCADE,
        status VARCHAR(20) DEFAULT 'pendente' CHECK (status IN ('pendente','aceita','em_andamento','completada','cancelada','falhou')),
        endereco_partida TEXT,
        endereco_entrega TEXT,
        distancia_estimada DECIMAL(6,2),
        tempo_estimado INTEGER,
        avaliacao_restaurante INTEGER CHECK (avaliacao_restaurante BETWEEN 1 AND 5),
        avaliacao_beneficiario INTEGER CHECK (avaliacao_beneficiario BETWEEN 1 AND 5),
        avaliacao_voluntario INTEGER CHECK (avaliacao_voluntario BETWEEN 1 AND 5),
        comentario_restaurante TEXT,
        comentario_beneficiario TEXT,
        comentario_voluntario TEXT,
        codigo_rastreamento VARCHAR(50),
        ultima_atualizacao_rota TIMESTAMP WITH TIME ZONE,
        data_criacao TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
        data_aceitacao TIMESTAMP WITH TIME ZONE,
        data_inicio TIMESTAMP WITH TIME ZONE,
        data_conclusao TIMESTAMP WITH TIME ZONE,
        data_cancelamento TIMESTAMP WITH TIME ZONE,
        UNIQUE(voluntario_id, doacao_id)
    );
    """)
    cur.execute("CREATE INDEX IF NOT EXISTS idx_missao_voluntario ON missoes(voluntario_id);")
    cur.execute("CREATE INDEX IF NOT EXISTS idx_missao_doacao ON missoes(doacao_id);")
    cur.execute("CREATE INDEX IF NOT EXISTS idx_missao_status ON missoes(status);")

    # =======================
    # Triggers para atualizar data_atualizacao
    # =======================
    cur.execute("""
    CREATE OR REPLACE FUNCTION atualizar_data_atualizacao()
    RETURNS TRIGGER AS $$
    BEGIN
        NEW.data_atualizacao = CURRENT_TIMESTAMP;
        RETURN NEW;
    END;
    $$ LANGUAGE plpgsql;
    """)

    for table in ["usuarios", "restaurantes", "beneficiarios", "voluntarios"]:
        cur.execute(f"""
        DROP TRIGGER IF EXISTS trigger_{table}_atualizacao ON {table};
        CREATE TRIGGER trigger_{table}_atualizacao
        BEFORE UPDATE ON {table}
        FOR EACH ROW
        EXECUTE FUNCTION atualizar_data_atualizacao();
        """)

    conn.commit()
    cur.close()
    conn.close()
    print("Banco FullBelly criado com sucesso!")

if __name__ == "__main__":
    create_tables()
