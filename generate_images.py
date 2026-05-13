import os
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import utils.clean_utils as clean_utils

def generar_plots_memoria1():
    individual_stats = pd.read_csv("datasets/individual_stats.csv", sep=",")
    individual_stats_10 = clean_utils.construct_valid_teams(individual_stats)
    team = individual_stats_10.groupby(["MatchId", "Win"]).agg(total_gold=("TotalGold", "sum"), total_minions=("MinionsKilled", "sum"), 
                                                               total_kills=("kills", "sum"), total_deaths=("deaths", "sum"), 
                                                               total_assists=("assists", "sum")).reset_index()
    
    metrics = {"total_gold": "Total Gold", "total_minions": "Minions Killed", "total_kills": "Kills", "total_deaths": "Deaths", 
               "total_assists": "Assists"}
    
    output_dir = "plots/violins_metrics"
    os.makedirs(output_dir, exist_ok=True)
    for col, label in metrics.items():
        fig, ax = plt.subplots(figsize=(5, 5))
        sns.violinplot(data=team, x="Win", y=col, hue="Win", split=True, inner="quart", ax=ax)

        ax.set_title(label)
        ax.set_xlabel("Win")
        ax.set_ylabel("")

        fig.tight_layout()

        fig.savefig(f"{output_dir}/{col}.png", dpi=300, bbox_inches="tight")

        plt.close(fig)
    
    # Segunda parte
    match_wide = team.pivot(index="MatchId", columns="Win", values=["total_gold", "total_minions", "total_kills", "total_deaths", 
                                                                    "total_assists"])

    # Compute winner minus loser differences
    match_wide["gold_diff"] = match_wide["total_gold"][1] - match_wide["total_gold"][0]
    match_wide["minions_diff"] = match_wide["total_minions"][1] - match_wide["total_minions"][0]
    match_wide["kills_diff"] = match_wide["total_kills"][1] - match_wide["total_kills"][0]
    match_wide["deaths_diff"] = match_wide["total_deaths"][1] - match_wide["total_deaths"][0]
    match_wide["assists_diff"] = match_wide["total_assists"][1] - match_wide["total_assists"][0]

    metrics_diff = {"Gold": "gold_diff", "Minions": "minions_diff", "Kills": "kills_diff", "Deaths": "deaths_diff", 
                    "Assists": "assists_diff"}

    win_rates = {}
    for name, col in metrics_diff.items():
        mask = match_wide[col] > 0  # Mark games where the team that won also has the advantage on the metric ( >0 ) 
        win_rate = mask.mean()  # Compute the average

        win_rates[name] = win_rate  # Store it

    labels = list(win_rates.keys())
    values = list(win_rates.values())

    colors = [
        "orange" if label in ["Kills", "Deaths", "Assists"] else "steelblue"
        for label in labels
    ]

    fig, ax = plt.subplots(figsize=(8, 5))

    ax.bar(labels, values, color=colors)

    ax.axhline(0.5, color="red", linestyle="--", label="50% baseline")

    ax.set_ylabel("Win rate cuando tiene la ventaja")
    ax.set_title("Como de probable es que el equipo con más X gane?")

    ax.legend()
    plt.xticks(rotation=15)
    ax.legend()

    fig.savefig("plots/winrate_advantage.png", dpi=300, bbox_inches="tight")
    plt.close(fig)

    # Tercera parte
    group_stats = pd.read_csv("datasets/group_stats.csv", sep=",")
    blue = group_stats[["MatchId", "BlueTowerKills", "BlueDragonKills", "BlueBaronKills", "BlueRiftHeraldKills", "BlueKills", "BlueWin"]].copy()
    blue.columns = ["MatchId", "TowerKills", "DragonKills", "BaronKills", "HeraldKills", "Kills", "Win"]

    red = group_stats[["MatchId", "RedTowerKills", "RedDragonKills","RedBaronKills", "RedRiftHeraldKills", "RedKills", "RedWin"]].copy()
    red.columns = ["MatchId", "TowerKills", "DragonKills", "BaronKills", "HeraldKills", "Kills", "Win"]

    team_stats = pd.concat([blue, red], ignore_index=True)
    team_stats["DragonKills"].value_counts()

    metrics = {"TowerKills": "Torres", "DragonKills": "Dragones", "BaronKills": "Barones", "Kills": "Kills"}

    fig, axes = plt.subplots(1, 2, figsize=(10, 6), gridspec_kw={"width_ratios": [5, 1]})

    corr_matrix = team_stats[list(metrics.keys()) + ["Win"]].corr()

    # Heatmap principal sin Win
    sns.heatmap(
        corr_matrix.drop("Win").drop("Win", axis=1),
        annot=True, fmt=".2f", cmap="BrBG", center=0,
        square=True, linewidths=0.5, ax=axes[0], cbar=False
    )
    axes[0].set_title("Correlación entre métricas")

    # Columna Win sola
    sns.heatmap(
        corr_matrix.drop("Win")[["Win"]],
        annot=True, fmt=".2f", cmap="BrBG", center=0,
        square=True, linewidths=0.5, ax=axes[1], cbar=True
    )
    axes[1].set_title("vs Win")
    axes[1].set_ylabel("")

    fig.suptitle("Correlación entre objetivos, combate y victoria", fontsize=13)
    plt.tight_layout()
    fig.savefig("plots/correlation_heatmap.png", dpi=300, bbox_inches="tight")
    plt.close(fig)

    # Cuarta parte
    fig, ax = plt.subplots(figsize=(9, 5))

    objective_cols = {"TowerKills": "Torres", "DragonKills": "Dragones", "BaronKills": "Barones"}

    for col, label in objective_cols.items():
        win_rate_by_obj = team_stats.groupby(col)["Win"].mean()
        ax.plot(win_rate_by_obj.index, win_rate_by_obj.values, marker="o", label=label)

    ax.axhline(0.5, color="red", linestyle="--", linewidth=0.8, label="50% baseline")
    ax.set_xlabel("Número de objetivos conseguidos")
    ax.set_ylabel("Win rate")
    ax.set_title("Win rate acumulado por número de objetivos")
    ax.xaxis.set_major_locator(plt.MultipleLocator(1))
    ax.legend()
    fig.tight_layout()
    fig.savefig("plots/winrate_objectives.png", dpi=300, bbox_inches="tight")
    plt.close(fig)

    return None


def generar_plots_memoria2():
    individual_stats = pd.read_csv("datasets/individual_stats.csv", sep=",")
    group_stats = pd.read_csv("datasets/group_stats.csv", sep=",")
    champion_tbl = pd.read_csv("datasets/ChampionTbl.csv", sep=",")
    rank_tbl = pd.read_csv("datasets/RankTbl.csv", sep=",")

    # Usar columnas "RankFk" y "ChampionFK"
    champ_cols = ["B1Champ", "B2Champ", "B3Champ", "B4Champ", "B5Champ", "R1Champ", "R2Champ", "R3Champ", "R4Champ", "R5Champ"]

    champs_melted = group_stats.melt(id_vars=["MatchId", "RankFk"], value_vars=champ_cols, value_name="Champion")
    champs_melted = champs_melted.drop(columns="variable")

    total_picks_per_rank = champs_melted.groupby("RankFk")["Champion"].count()  # Total number of champion picks in each rank

    champ_picks = champs_melted.groupby(["RankFk", "Champion"])["Champion"].count()  # Number of each champion picks in each rank

    pick_rate = (champ_picks / total_picks_per_rank)
    pick_rate = pick_rate.rename("PickRate").reset_index()  # Create a dataframe

    top_n = 3
    pick_rate_sorted = pick_rate.sort_values(["RankFk", "PickRate"], ascending=[True, False])
    top_n_champs_pickrate = pick_rate_sorted.groupby("RankFk").head(top_n)

    top_n_champs_pickrate = pd.merge(top_n_champs_pickrate, rank_tbl, left_on="RankFk", right_on="RankId")
    top_n_champs_pickrate = pd.merge(top_n_champs_pickrate, champion_tbl, left_on="Champion", right_on="ChampionId")
    top_n_champs_pickrate = top_n_champs_pickrate.drop(columns=["RankFk", "RankId", "ChampionId", "Champion"])
    top_n_champs_pickrate

    rank_order = ["Unranked", "Iron", "Bronze", "Silver", "Gold", "Platinum", "Emerald", "Diamond", "Master", "Grandmaster", "Challenger"]
    top_n_champs_pickrate["RankName"] = pd.Categorical(top_n_champs_pickrate["RankName"], categories=rank_order, ordered=True)
    top_n_champs_pickrate = top_n_champs_pickrate.sort_values("RankName")
    top_n_champs_pickrate_ranked = top_n_champs_pickrate[top_n_champs_pickrate["RankName"] != "Unranked"]

    heatmap_df = top_n_champs_pickrate_ranked.pivot(index="ChampionName", columns="RankName",values="PickRate")
    heatmap_df = heatmap_df.fillna(0)

    g = sns.clustermap(heatmap_df, cmap="rocket_r", linewidths=0.5, figsize=(7, 6), metric="euclidean", method="average", 
                       col_cluster=False)
    g.savefig("plots/champion_clustermap.png", dpi=300, bbox_inches="tight")
    plt.close()

    # Segunda parte
    df = pick_rate.copy()
    df = df.sort_values(["RankFk", "PickRate"], ascending=[True, False])

    df["pos"] = df.groupby("RankFk").cumcount() + 1
    df["cum_pick"] = df.groupby("RankFk")["PickRate"].cumsum()
    df["total"] = df.groupby("RankFk")["PickRate"].transform("sum")
    df["cum_share"] = df["cum_pick"] / df["total"]

    df = pd.merge(df, rank_tbl, left_on="RankFk", right_on="RankId")
    df = df.drop(columns=["RankFk", "RankId"])
    df= df[df["RankName"] != "Unranked"]

    fig = plt.figure(figsize=(10,6))

    sns.lineplot(data=df, x="pos", y="cum_share", hue="RankName")

    plt.title("Curva de concentración del meta por rango")
    plt.xlabel("Número de campeones (ordenados por pick rate)")
    plt.ylabel("Pick rate acumulado")
    plt.ylim(0, 1)
    fig.tight_layout()

    fig.savefig("plots/meta_concentration_curve.png", dpi=300, bbox_inches="tight")

    plt.close(fig)

    # Tercera parte
    duration_stats = group_stats[["MatchId", "RankFk", "GameDuration"]]
    duration_stats = duration_stats[(duration_stats["GameDuration"] > 300) & (duration_stats["GameDuration"] < 3600)]
    duration_stats = duration_stats[duration_stats["RankFk"] != 0]
    duration_stats = duration_stats.merge(rank_tbl, left_on="RankFk", right_on="RankId")
    duration_stats["GameDurationMin"] = duration_stats["GameDuration"] / 60

    rank_order = ["Iron", "Bronze", "Silver", "Gold", "Platinum", "Emerald", "Diamond", "Master", "Grandmaster", "Challenger"]

    fig, ax = plt.subplots(figsize=(12, 5))
    sns.boxplot(data=duration_stats, x="RankName", y="GameDurationMin", order=rank_order, hue="RankName")
    ax.set_xlabel("Rango")
    ax.set_ylabel("Duración (minutos)")
    ax.set_title("Distribución de duración de partidas por rango")
    plt.xticks(rotation=25)
    fig.tight_layout()

    fig.savefig("plots/game_duration_by_rank.png", dpi=300, bbox_inches="tight")

    plt.close(fig)

    # Cuarta parte
    group_stats2 = group_stats.copy()
    group_stats2["TotalKills"] = group_stats2["BlueKills"] + group_stats2["RedKills"]
    group_stats2["TotalTowers"] = group_stats2["BlueTowerKills"] + group_stats2["RedTowerKills"]
    group_stats2["TotalDragons"] = group_stats2["BlueDragonKills"] + group_stats2["RedDragonKills"]
    group_stats2["TotalBarons"] = group_stats2["BlueBaronKills"] + group_stats2["RedBaronKills"]
    group_stats2["GameDurationMin"] = group_stats2["GameDuration"] / 60

    group_stats2["KillsPerMin"] = group_stats2["TotalKills"] / group_stats2["GameDurationMin"]
    group_stats2["ObjPerMin"] = (group_stats2["TotalTowers"] + group_stats2["TotalDragons"] + group_stats2["TotalBarons"]) / group_stats2["GameDurationMin"]
    group_stats2["ObjCombatRatio"] = group_stats2["ObjPerMin"] / group_stats2["KillsPerMin"]

    rank_order = ["Iron", "Bronze", "Silver", "Gold", "Platinum", "Emerald", "Diamond", "Master", "Grandmaster", "Challenger"]
    group_stats2 = group_stats2[group_stats2["RankFk"] != 0]
    group_ranked = pd.merge(group_stats2, rank_tbl, left_on="RankFk", right_on="RankId")

    rank_means = group_ranked.groupby("RankName")[["KillsPerMin", "ObjPerMin"]].mean().reindex(rank_order)

    fig, axes = plt.subplots(1, 2, figsize=(12, 5))

    axes[0].plot(rank_order, rank_means["KillsPerMin"], marker="o", color="salmon")
    axes[0].set_title("Kills por minuto por rango")
    axes[0].set_xlabel("Rango")
    axes[0].set_ylabel("Kills / min")
    axes[0].tick_params(axis="x", rotation=25)

    axes[1].plot(rank_order, rank_means["ObjPerMin"], marker="o", color="steelblue")
    axes[1].set_title("Objetivos por minuto por rango")
    axes[1].set_xlabel("Rango")
    axes[1].set_ylabel("Objetivos / min")
    axes[1].tick_params(axis="x", rotation=25)

    fig.suptitle("Kills vs Objetivos por minuto según rango", fontsize=13)
    plt.tight_layout()
    
    fig.savefig("plots/rank_kills_vs_objectives.png", dpi=300, bbox_inches="tight")

    plt.close(fig)
    return None


def generar_plots_memoria3():
    individual_stats = pd.read_csv("datasets/individual_stats.csv", sep=",")
    individual_stats["CurrentMasteryPoints"].value_counts().sort_index()

    mastery_df = individual_stats[(individual_stats["RankFk"] != 0) & (individual_stats["CurrentMasteryPoints"] > 0)]
    mastery_df["MasterySegments"] = pd.qcut(mastery_df["CurrentMasteryPoints"], q=4, 
                                        labels=["Q1 (Baja)", "Q2 (Media-Baja)", "Q3 (Media-Alta)", "Q4 (Alta)"])
    metrics = ["kills", "deaths", "assists", "DmgDealt", "Win"]
    perf = mastery_df.groupby("MasterySegments")[metrics].agg(["mean", "std"]).round(3)

    std_df = mastery_df.groupby("MasterySegments")[["kills", "deaths", "assists", "DmgDealt"]].std().reset_index()

    fig, axes = plt.subplots(1, 4, figsize=(18, 5))

    metric_labels = {"kills": "Kills", "deaths": "Deaths", "assists": "Assists", "DmgDealt": "Daño"}

    for ax, (col, label) in zip(axes, metric_labels.items()):
        ax.bar(std_df["MasterySegments"], std_df[col], color="steelblue")
        ax.set_title(label)
        ax.set_xlabel("")
        ax.set_ylabel("Desviación estándar" if ax == axes[0] else "")
        ax.tick_params(axis="x", rotation=25)

    fig.suptitle("Consistencia del rendimiento por nivel de maestría\n(menor desviación = más consistente)", fontsize=13)
    plt.tight_layout()
    fig.savefig("plots/mastery_consistency_std.png", dpi=300, bbox_inches="tight")
    plt.close(fig)

    return None


def generar_plots_memoria4():
    individual_stats = pd.read_csv("datasets/individual_stats.csv", sep=",")
    rank_tbl = pd.read_csv("datasets/RankTbl.csv", sep=",")

    role_df = individual_stats[individual_stats["Lane"] != "NONE"]
    role_df["Lane"] = role_df["Lane"].replace("UTILITY", "SUPPORT")

    metrics = ["kills", "deaths", "assists", "DmgDealt", "DmgTaken", "TurretDmgDealt", "TotalGold", "MinionsKilled", "visionScore"]
    role_means = role_df.groupby("Lane")[metrics].mean()  # Mean per role for each metric

    role_normalized = (role_means - role_means.min()) / (role_means.max() - role_means.min())  # Normalize 0-1
    role_normalized = role_normalized * 0.8 + 0.2  # rescale to 0.2-1.0 instead of 0-1 so it does not collapse low values to 0

    # Radar chart
    labels = metrics
    num_vars = len(labels)
    angles = np.linspace(0, 2 * np.pi, num_vars, endpoint=False).tolist()
    angles += angles[:1]  # close the polygon

    colors = {"TOP": "steelblue", "JUNGLE": "green", "MIDDLE": "red", "BOTTOM": "orange", "SUPPORT": "purple"}
    roles_order = ["TOP", "JUNGLE", "MIDDLE", "BOTTOM", "SUPPORT"]

    output_dir = "plots/radar_roles"
    os.makedirs(output_dir, exist_ok=True)
    for role in roles_order:
        fig, ax = plt.subplots(figsize=(5, 5), subplot_kw={"polar": True})

        row = role_normalized.loc[role]
        values = row.tolist() + row.tolist()[:1]

        ax.plot(angles, values, color=colors[role], linewidth=2)
        ax.fill(angles, values, color=colors[role], alpha=0.25)

        ax.set_xticks(angles[:-1])
        ax.set_xticklabels(labels, size=8)
        ax.set_ylim(0, 1.1)
        ax.set_yticks([])

        ax.tick_params(pad=12) 
        ax.set_title(role, size=12, pad=15, color=colors[role])

        fig.subplots_adjust(top=0.88, bottom=0.05)

        fig.savefig(f"{output_dir}/radar_{role}.png", dpi=300, bbox_inches="tight")

        plt.close(fig)

    # Segunda parte
    metrics_style = ["kills", "deaths", "assists", "visionScore", "MinionsKilled", "TurretDmgDealt"]
    rank_order = ["Iron", "Bronze", "Silver", "Gold", "Platinum", "Emerald", "Diamond", "Master", "Grandmaster", "Challenger"]

    role_rank_df = role_df[role_df["RankFk"] != 0]  # Remove unranked
    role_rank_df = role_rank_df[role_rank_df["Lane"] != "SUPPORT"]
    role_rank_df = pd.merge(role_rank_df, rank_tbl, left_on="RankFk", right_on="RankId")
    role_rank_means = role_rank_df.groupby(["Lane", "RankName"])[metrics_style].mean()  # Media por rango

    metrics_style = {"kills": "Kills", "deaths": "Deaths", "assists": "Assists", "DmgDealt": "Daño Realizado", 
                     "DmgTaken": "Daño Recibido", "TurretDmgDealt": "Turret Dmg", "MinionsKilled": "Minions", 
                     "visionScore": "Vision Score"}

    role_rank_means = role_rank_df.groupby(["Lane", "RankName"])[list(metrics_style.keys())].mean()

    roles = ["TOP", "JUNGLE", "MIDDLE", "BOTTOM"]
    role_colors = {"TOP": "steelblue", "JUNGLE": "green", "MIDDLE": "red", "BOTTOM": "orange"}

    output_dir = "plots/evolution_roles_ranks"
    os.makedirs(output_dir, exist_ok=True)

    for metric, label in metrics_style.items():
        fig, ax = plt.subplots(figsize=(6, 4))
        for role in roles:
            values = [role_rank_means.loc[(role, rank), metric] for rank in rank_order]
            ax.plot(rank_order, values, marker="o", label=role, color=role_colors[role], markersize=4)

        ax.set_title(label)
        ax.set_xlabel("Rango")
        ax.set_ylabel("Media")
        ax.tick_params(axis="x", rotation=30)
        ax.legend(fontsize=7)

        fig.tight_layout()

        fig.savefig(f"{output_dir}/{metric}.png", dpi=300, bbox_inches="tight")

        plt.close(fig)

    return None



os.makedirs("plots", exist_ok=True)
generar_plots_memoria1()
generar_plots_memoria2()
generar_plots_memoria3()
generar_plots_memoria4()