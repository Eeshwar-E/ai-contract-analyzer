const ClauseCard = ({ data }) => {
  const riskLevel = data.risk?.level || "Low";

  const getColor = () => {
    if (riskLevel === "High") return "#ff4d4f";
    if (riskLevel === "Medium") return "#faad14";
    return "#52c41a";
  };

  return (
    <div
      style={{
        background: "#fff",
        borderRadius: "10px",
        padding: "16px",
        marginBottom: "16px",
        boxShadow: "0 2px 8px rgba(0,0,0,0.08)",
        borderLeft: `6px solid ${getColor()}`
      }}
    >
      <p style={{ marginBottom: "10px" }}>
        <strong>Clause:</strong>
        <br />
        {data.clause}
      </p>

      <div style={{ marginBottom: "12px" }}>
        <strong>Predictions:</strong>

        <div style={{ marginTop: "8px" }}>
          {(data.predictions || []).map((pred, idx) => (
            <div
              key={idx}
              style={{
                display: "inline-block",
                marginRight: "10px",
                marginBottom: "8px",
                background: "#f5f5f5",
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
            backgroundColor: getColor(),
            color: "#fff",
            padding: "4px 10px",
            borderRadius: "6px",
            fontSize: "12px"
          }}
        >
          {riskLevel}
        </span>

        {"  "}

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
    </div>
  );
};

export default ClauseCard;