package com.example;

public class GameTerritory {
    public int territoryId;

    public int troops;

    public String owner;

    public GameTerritory(int territoryId, int troops, String owner) {
        this.territoryId = territoryId;
        this.troops = troops;
        this.owner = owner;
    }

    public int getTerritoryId() {
        return this.territoryId;
    }

    public void setTerritoryId(int territoryId) {
        this.territoryId = territoryId;
    }

    public int getTroops() {
        return this.troops;
    }

    public void setTroops(int troops) {
        this.troops = troops;
    }

    public String getOwner() {
        return this.owner;
    }

    public void setOwner(String owner) {
        this.owner = owner;
    }
}
