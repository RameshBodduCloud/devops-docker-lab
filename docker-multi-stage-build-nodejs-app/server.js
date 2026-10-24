const express = require("express");

const app = express();

const PORT = 3000;

app.get("/", (req, res) => {
    res.send("Hello! Docker Multi-Stage Build Working!");
});

app.get("/health", (req, res) => {
    res.json({
        status: "UP",
        message: "Application running successfully"
    });
});

app.listen(PORT, "0.0.0.0", () => {
    console.log(`Server running on port ${PORT}`);
});
