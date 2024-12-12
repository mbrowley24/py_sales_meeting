// Define the network graph
const graph = {
    A: { B: 2, C: 4 },
    B: { A: 2, C: 1, D: 7, E: 3 },
    C: { A: 4, B: 1, D: 2 },
    D: { B: 7, C: 2, E: 1 },
    E: { B: 3, D: 1 }
};

// Dijkstra's Algorithm for shortest path calculation
function dijkstra(graph, start) {
    const distances = {};
    const visited = new Set();
    const previous = {};

    // Initialize distances with Infinity
    for (let node in graph) {
        distances[node] = Infinity;
    }
    distances[start] = 0;

    while (visited.size < Object.keys(graph).length) {
        const currentNode = getClosestNode(distances, visited);
        visited.add(currentNode);

        for (let neighbor in graph[currentNode]) {
            const newDistance = distances[currentNode] + graph[currentNode][neighbor];
            if (newDistance < distances[neighbor]) {
                distances[neighbor] = newDistance;
                previous[neighbor] = currentNode;
            }
        }
    }
    return { distances, previous };
}

// Find the closest unvisited node
function getClosestNode(distances, visited) {
    return Object.keys(distances).reduce((closest, node) => {
        if (!visited.has(node) && (closest === null || distances[node] < distances[closest])) {
            return node;
        }
        return closest;
    }, null);
}

// Visualize the path with SVG lines
function visualizePath(path) {
    const network = document.getElementById("network");
    const nodes = path.reverse();

    nodes.forEach((node, index) => {
        if (index > 0) {
            const previousNode = document.getElementById(nodes[index - 1]);
            const currentNode = document.getElementById(node);

            const line = document.createElementNS("http://www.w3.org/2000/svg", "line");
            line.setAttribute("x1", previousNode.offsetLeft + 25);
            line.setAttribute("y1", previousNode.offsetTop + 25);
            line.setAttribute("x2", currentNode.offsetLeft + 25);
            line.setAttribute("y2", currentNode.offsetTop + 25);
            line.setAttribute("class", "link");

            const svg = document.createElementNS("http://www.w3.org/2000/svg", "svg");
            svg.appendChild(line);
            network.appendChild(svg);
        }
    });
}

// Trigger the shortest path calculation
function calculateShortestPath() {
    const { distances, previous } = dijkstra(graph, "A");
    const target = "E";
    const path = [];

    let currentNode = target;
    while (currentNode) {
        path.push(currentNode);
        currentNode = previous[currentNode];
    }

    alert(`Shortest path from A to E: ${path.reverse().join(" → ")}\nDistance: ${distances[target]}`);
    visualizePath(path);
}
