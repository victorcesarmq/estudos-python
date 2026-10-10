CREATE VIEW ranking_municipios AS
SELECT "unidadeOrgao.municipioNome" AS municipio, SUM(valorTotalEstimado) AS total_estimado, SUM(valorTotalHomologado) as total_homologado
FROM licitacoes
GROUP BY municipio
ORDER BY total_homologado DESC

CREATE VIEW view_ranking_orgaos AS
SELECT "unidadeOrgao.nomeUnidade" AS orgao, SUM(valorTotalEstimado) AS total_estimado, SUM(valorTotalHomologado) as total_homologado
FROM licitacoes
GROUP BY orgao
ORDER BY total_homologado DESC