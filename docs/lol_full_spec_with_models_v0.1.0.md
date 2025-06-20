# 🗉 Full System Architecture with Pydantic Models

This document defines the complete, interface-driven architecture for the LoL Game Insight system, including:

- Layered responsibilities
- Interfaces between layers
- Shared structured data models using `pydantic`
- Integration point for LLM-based subjective analysis
- Support for both **live** and **latest historical** match analysis

---

## 📚 System Layers

```plaintext
[ Presentation Layer ]
    ↑
[ Application Layer (Analyzers) ]
    ↑
[ LLM Analysis Layer ]   ← Subjective evaluation (LLM-based)
    ↑
[ Data Layer (Riot API + Data Dragon) ]
```

---

## (truncated preview...)