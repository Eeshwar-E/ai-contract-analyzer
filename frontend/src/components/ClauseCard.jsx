const ClauseCard = ({ data }) => {
  const riskLevel = data.risk?.level || "Low";

  const getRiskColor = () => {
    if (riskLevel === "High") return "#ff4d4f";
    if (riskLevel === "Medium") return "#faad14";
    return "#52c41a";
  };

  const getPredictionColor = (confidence) => {
    if (confidence >= 0.8) return "#52c41a";
    if (confidence >= 0.55) return "#faad14";
    return "#bfbfbf";
  };

  return (
    <div
      style={{
        background: "#fff",
        borderRadius: "10px",
        padding: "16px",
        marginBottom: "16px",
        boxShadow: "0 2px 8px rgba(0,0,0,0.08)",
        borderLeft: `6px solid ${getRiskColor()}`
      }}
    >
      <p style={{ marginBottom: "10px" }}>
        <strong>Clause:</strong>
        <br />
        {data.clause}
      </p>

      <div style={{ marginBottom: "12px" }}>
        <strong>
          {(data.predictions?.[0]?.confidence || 0) < 0.5
            ? "Possible Categories:"
            : "Predictions:"}
        </strong>

        <div style={{ marginTop: "8px" }}>
          {(data.predictions || []).map((pred, idx) => (
            <div
              key={idx}
              style={{
                display: "inline-block",
                marginRight: "10px",
                marginBottom: "8px",
                background: "#f5f5f5",
                border: `1px solid ${getPredictionColor(pred.confidence)}`,
                padding: "6px 10px",
                borderRadius: "6px",
                fontSize: "13px"
              }}
            >
              <strong>{pred.label}</strong>{" "}
              ({Math.round((pred.confidence || 0) * 100)}%)
            </div>
          ))}
        </div>
      </div>

      <p>
        <strong>Risk:</strong>{" "}
        <span
          style={{
            backgroundColor: getRiskColor(),
            color: "#fff",
            padding: "4px 10px",
            borderRadius: "6px",
            fontSize: "12px"
          }}
        >
          {riskLevel}
        </span>

        <span
          style={{
            marginLeft: "8px",
            background: "#f0f0f0",
            padding: "4px 8px",
            borderRadius: "5px",
            fontSize: "12px"
          }}
        >
          {Math.round((data.risk?.confidence || 0) * 100)}%
        </span>
      </p>

      <p>
        <strong>Explanation:</strong>{" "}
        {data.explanation}
      </p>
      {data.phrases?.length > 0 && (
        <div style={{ marginTop: "10px" }}>
          <strong>Risk Phrases:</strong>

          <div style={{ marginTop: "8px" }}>
            {data.phrases.map((phrase, idx) => (
              <span
                key={idx}
                style={{
                  display: "inline-block",
                  background: "#fff1f0",
                  color: "#cf1322",
                  padding: "4px 8px",
                  borderRadius: "6px",
                  marginRight: "8px",
                  marginBottom: "8px",
                  fontSize: "12px"
                }}
              >
                {phrase}
              </span>
            ))}
          </div>
        </div>
      )}
    </div>
  );
};

export default ClauseCard;