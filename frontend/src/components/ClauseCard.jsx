const ClauseCard = ({ data }) => {
  const getColor = () => {
    if (data.risk === "High") return "#ff4d4f";
    if (data.risk === "Medium") return "#faad14";
    return "#52c41a";
  };

  return (
    <div style={{
      background: "#fff",
      borderRadius: "10px",
      padding: "16px",
      marginBottom: "16px",
      boxShadow: "0 2px 8px rgba(0,0,0,0.08)",
      borderLeft: `6px solid ${getColor()}`
    }}>
      <p style={{ marginBottom: "10px" }}>
        <strong>Clause:</strong><br />
        {data.clause}
      </p>

      <p><strong>Type:</strong> {data.type}</p>
      <p>
        <strong>Confidence:</strong>{" "}
        <span style={{
            background: "#f0f0f0",
            padding: "4px 8px",
            borderRadius: "5px",
            fontSize: "12px"
        }}>
            {(data.confidence * 100).toFixed(0)}%
        </span>
      </p>
      <p>
        <strong>Risk:</strong>{" "}
        <span style={{
          backgroundColor: getColor(),
          color: "#fff",
          padding: "4px 10px",
          borderRadius: "6px",
          fontSize: "12px"
        }}>
          {data.risk}
        </span>
      </p>

      <p><strong>Explanation:</strong> {data.explanation}</p>
    </div>
  );
};

export default ClauseCard;