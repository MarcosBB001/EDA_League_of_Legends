# League of Legends Match Data EDA

<p align="left">
  <img src="summoner_rift.jpg" alt="LoL banner" width="500"/>
</p>

## 📌 Descripción del proyecto

*League of Legends* es un videojuego multijugador en línea del género *MOBA* (*Multiplayer Online Battle Arena*) desarrollado por *Riot Games*. En cada partida, dos equipos de cinco jugadores se enfrentan en un mapa simétrico con el objetivo de destruir el *nexo* del equipo rival. Cada jugador controla un *campeón* único y ocupa un rol específico dentro del equipo (*top*, *jungle*, *mid*, *bottom* o *support*). A lo largo de la partida, cada jugador acumula recursos (oro, *kills*, minions eliminados, objetivos neutrales) que determinan su capacidad de impactar el resultado. El juego cuenta con dos modalidades principales: 
- Partidas ***Ranked***, en las que los jugadores compiten por ascender en un sistema de rangos (desde *Iron* hasta *Challenger*). 
- Partidas **Casuales**, sin repercusión en la clasificación.

Este proyecto consiste en un análisis exploratorio de datos (*EDA*) sobre un conjunto de aproximadamente 200.000 partidas del modo *Classic* de *League of Legends*, con el objetivo de identificar qué factores están más asociados al resultado de una partida, analizando tanto el rendimiento individual como el colectivo.

## 📊 Datos:
Los datos analizados contienen la información de 270.000+ partidas de *League of Legends* jugadas entre los parches **15.17 y 16.01**.

Se organizan en dos grupos principales:

---

### 🧠 Datos principales del juego

- **MatchStatsTbl.csv**: estadísticas individuales de cada jugador en una partida (oro, daño, KDA, items, etc.)
- **TeamMatchTbl.csv**: estadísticas agregadas por equipo (objetivos, composición, resultado de la partida, etc.)
- **MatchTbl.csv**: información general de la partida (modo de juego, duración, rango medio, etc.)

---

### 🔗 Tablas de relación y mapeo

- **SummonerMatchTbl.csv**: relación entre jugador, partida y campeón utilizado
- **ChampionTbl.csv**: mapeo de ID de campeón a nombre
- **RankTbl.csv**: mapeo de ID de rango a nombre
- **ItemTbl.csv**: mapeo de ID de objeto a nombre


Los datasets han sido extraídos mediante la API pública de Riot Games y publicados en Kaggle por Nathan Smallcalder. 

Pueden descargarse en esta fuente: [enlace](https://www.kaggle.com/datasets/nathansmallcalder/lol-match-history-and-summoner-data-80k-matches)

## 🧪 Hipótesis

A lo largo del análisis se explorarán distintas hipótesis sobre el comportamiento y las dinámicas de juego en las partidas:

### 🏆 Factores relacionados con la victoria
- Las métricas económicas (oro y minions) tienen una relación más fuerte con la victoria que las métricas de combate (kills, deaths y assists).
- El control de objetivos grupal (torres, dragones y barones) está más asociado al resultado de la partida que las estadísticas individuales de combate.

### 🏅 Tipo de partida y nivel de juego
- Las partidas ranked presentan un estilo de juego más serio (eficiente) que las partidas casuales.
    - Las partidas casuales presentan más diversidad de campeones que las ranked.
    - La duración de las partidas varía según el rango.
- El comportamiento de los jugadores (kills, muertes, duración de partidas) varía en función del nivel medio de la partida.
- En partidas de mayor rango medio, los equipos priorizan más los objetivos que el combate directo.

### 🧩 Maestría y experiencia con campeones
- Los jugadores con mayor maestría sobre un campeón presentan un rendimiento más consistente.
- La relación entre maestría sobre un campeón y el rendimiento es más pronunciada en rangos altos que en rangos bajos.

### 🛡️ Diferencias entre roles
- Las métricas de rendimiento varían significativamente según el rol del jugador.
- El estilo de juego de cada rol cambia en función del nivel medio de la partida.

<p align="left">
  <img src="roles.png" alt="LoL roles" width="700"/>
</p>