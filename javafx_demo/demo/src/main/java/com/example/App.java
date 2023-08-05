package com.example;

import java.util.Arrays;
import java.util.Collections;
import java.util.List;
import java.util.stream.Collectors;
import java.util.stream.IntStream;

public class App {

    public static void main(String[] args) {

    }

    public static void makeThings() {
        GameTerritory[] territories = divideTerritories(players, n);

        int troopsPerPlayer = 50 - players.length * 5;

        for (Player p : players) {
            GameTerritory[] ownedTerritories = Arrays.stream(territories).filter(t -> t.getOwner().equals(p.getId()))
                    .toArray(GameTerritory[]::new);

            int troopsLeft = troopsPerPlayer - ownedTerritories.length;
            while (troopsLeft > 0) {
                int rand = (int) (Math.random() * ownedTerritories.length);
                ownedTerritories[rand].troops++;
                troopsLeft--;
            }
        }
        return territories;
    }

    public GameTerritory[] divideTerritories(Player[] players, int numTerritories) {
        GameTerritory[] territories = new GameTerritory[numTerritories];
        List<Integer> order = generateRandomOrder(numTerritories);

        for (int x = 0; x < territories.length / players.length; x++) {
            for (int y = 0; y < players.length; y++) {
                int i = x * players.length + y;
                if (i >= numTerritories)
                    break;
                territories[order.get(i)] = new GameTerritory(order.get(i), 1, players[y].getId());
            }
        }

        return territories;
    }
}