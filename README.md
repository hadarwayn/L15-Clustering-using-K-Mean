# L15: Interactive K-Means Clustering Educational Simulator

![K-Means Simulator Banner](https://i.imgur.com/example.png) <!-- Placeholder: A banner image would go here -->

**Welcome to the Interactive K-Means Clustering Simulator!** This educational tool transforms the abstract theory of K-Means clustering into a tangible, visual, and interactive learning experience. It is designed for students, developers, and data science enthusiasts who want to build a deep, intuitive understanding of how this fundamental unsupervised learning algorithm behaves.

This project was developed as a part of the "AI Developer Expert" course, referencing Dr. Yoram Segal's "K-MEAN Book v2.0".

---

## 🎯 Educational Goals

The primary goal of this simulator is to bridge the gap between the mathematical formulation of K-Means and its practical application. By using this tool, you will learn to:

- **Visualize the Algorithm:** Observe the iterative nature of K-Means (Assignment and Update steps) in action.
- **Understand Key Concepts:** Intuitively grasp what *centroids*, *inertia (WCSS)*, and *silhouette scores* represent.
- **Explore Failure Modes:** Discover why K-Means struggles with non-spherical clusters, varied densities, and overlapping data.
- **Develop Intuition:** Build a "feel" for how initial conditions and data distribution affect clustering outcomes.
- **Connect Theory to Practice:** See the direct link between the algorithm's assumptions and the final results.

---

## ✨ Features

- **Interactive Canvas:** Drag-and-drop entire groups of data points to see how their position affects clustering.
- **Variance Control:** "Explode" groups to increase their variance and observe how K-Means handles less-defined clusters.
- **Dual-Color Visualization:** Instantly compare the original "ground truth" (fill color) with the K-Means cluster assignment (edge color).
- **Detailed Analysis:** A comprehensive results panel provides not just metrics, but clear, educational explanations of what they mean in context.
- **Real-Time Feedback:** The GUI provides instant feedback on metrics and cluster assignments after every experiment.
- **Exportable Results:** Each experiment's plot and a detailed explanation are automatically saved to the `results` folder for your review.

---

## 🚀 Installation and Setup

Follow these steps to get the simulator running on your local machine.

### 1. Prerequisites

- [Python 3.10+](https://www.python.org/downloads/)
- [Git](https://git-scm.com/downloads/)

### 2. Clone the Repository

Open your terminal or command prompt and run the following command:

```bash
git clone https://github.com/hadarwayn/L15-Clustering-using-K-Mean.git
cd L15-HomeAssignment-K-Mean-Clustering
```

### 3. Set Up a Virtual Environment

It is highly recommended to use a virtual environment to manage project dependencies.

```bash
# Create a virtual environment
python -m venv .venv

# Activate the virtual environment
# On Windows:
.venv\Scripts\activate
# On macOS/Linux:
source .venv/bin/activate
```

### 4. Install Dependencies

Install the required Python libraries using the `requirements.txt` file.

```bash
pip install -r requirements.txt
```

### 5. Run the Application

You are now ready to launch the simulator!

```bash
python src/main.py
```

The application window should appear, displaying the initial state of the three Gaussian data groups.

---

## 🕹️ How to Use the Simulator

The simulator is composed of two main areas: the **Control Panel** on the left and the **Visualization Canvas** on the right.

![Simulator GUI Layout](https://i.imgur.com/example2.png) <!-- Placeholder: A screenshot of the GUI -->

### Controls

1.  **Select Group:** Choose which group (`A`, `B`, or `C`) you want to manipulate.
2.  **Explode Variance:**
    -   Use the **slider** to set a variance multiplier (1.0x to 5.0x).
    -   Click **"Explode Selected Group"** to increase the spread of the chosen group.
3.  **Run Clustering:** Click **"Run K-Means (K=3)"** to perform the clustering on the current data distribution.
4.  **Reset:** Click **"Start Over"** to reset all groups to their original positions and variances.
5.  **Status & Results:** The panels at the bottom provide status updates and detailed explanations of the clustering results.

### Visualization

-   **Points:** Each point's **fill color** is its "ground truth" group. After running K-Means, the **edge color** shows the cluster it was assigned to.
-   **True Means:** The large, semi-transparent 'X' markers show the actual centers of the original Gaussian groups.
-   **K-Means Centroids:** The large, solid black 'X' markers show the final centroids calculated by the K-Means algorithm.

---

## 🔬 Experiment Examples

Here are a few experiments you can run to build your intuition.

### Experiment 1: The Ideal Scenario (Perfect Separation)

**Goal:** See how K-Means performs when the data is perfectly separated.

1.  **Action:** Launch the application and click **"Run K-Means (K=3)"** without making any changes.
2.  **Observation:**
    -   The edge colors of the points will perfectly match their fill colors.
    -   The K-Means centroids (black 'X') will be almost directly on top of the true means (colored 'X').
    -   The **Silhouette Score** in the results panel will be high (e.g., > 0.75).
    -   The explanation will state that the clustering is "EXCELLENT".

    ![Perfect Separation](results/experiment_1_plot.png)

3.  **Learning:** In an ideal case where clusters are spherical and well-separated, K-Means is highly effective at identifying the underlying structure of the data.

### Experiment 2: Creating Overlap

**Goal:** Understand how K-Means handles ambiguity.

1.  **Action:**
    -   Click and drag the center of **Group A (Orange)** close to the center of **Group B (Blue)**.
    -   Click **"Run K-Means (K=3)"**.
2.  **Observation:**
    -   You will see some orange points now have a blue edge, and some blue points may have an orange edge. These are **misclassifications**.
    -   The K-Means centroids for these two clusters will have **drifted** away from their true means, moving towards the area of overlap.
    -   The **Silhouette Score** will drop significantly (e.g., to ~0.5).
    -   The explanation will highlight the "MODERATE" clustering quality and point out the centroid drift.

    ![Moderate Overlap](results/experiment_2_plot.png)

3.  **Learning:** K-Means does not know about the "ground truth" colors. It only sees a collection of points and tries to minimize the distance of each point to its assigned centroid. When groups overlap, K-Means creates a boundary based purely on distance, leading to misclassifications and a compromised "middle-ground" centroid.

### Experiment 3: The Exploded Group (High Variance)

**Goal:** See what happens when a cluster is not dense and spherical.

1.  **Action:**
    -   Click **"Start Over"** to reset.
    -   In the "Select Group" dropdown, choose **Group C (Green)**.
    -   Set the "Variance Multiplier" slider to **3.0x**.
    -   Click **"Explode Selected Group"**.
    -   Click **"Run K-Means (K=3)"**.
2.  **Observation:**
    -   The green points of Group C will be spread out widely.
    -   K-Means will likely **split** Group C, assigning some of its points to the orange cluster and some to the blue cluster. The edge colors on the green points will be mixed.
    -   The **Silhouette Score** will be low (< 0.5), indicating poor clustering.
    -   The explanation will describe this as "POOR CLUSTERING" and may point out that one group was split.

    ![Exploded Group](results/experiment_3_plot.png)

3.  **Learning:** K-Means assumes clusters are spherical and isotropic (equally spread in all directions). When a group has high variance, it violates this assumption. The algorithm incorrectly determines that it is more "efficient" (in terms of minimizing total squared distance) to assign the spread-out points to the neighboring, denser clusters rather than keeping them together.

---

## 📈 Understanding the Metrics

-   **Inertia (WCSS):** The sum of squared distances of samples to their closest cluster center. *Lower is generally better*, but this number always decreases as K (the number of clusters) increases, so it's not useful in isolation.
-   **Silhouette Score:** Measures how similar a point is to its own cluster compared to other clusters. It ranges from -1 to 1.
    -   `~1`: The point is well-clustered.
    -   `~0`: The point is on the boundary between two clusters.
    -   `-1`: The point is likely misclassified.
-   **Between-Cluster Scatter (BCS):** A measure of how far apart the clusters are from each other. Maximizing BCS is equivalent to minimizing Inertia.

---

## 🛠️ Future Enhancements

This project is a solid foundation. Future versions could include:

-   **Variable K:** A slider to change the number of clusters (K).
-   **Elbow Method Plot:** A feature to help determine the optimal value of K.
-   **Step-by-Step Animation:** Animate the assignment and update steps of the algorithm.
-   **Different Algorithms:** Add other clustering algorithms like DBSCAN or K-Medoids for comparison.

---

## 📜 License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.

---

*Happy Clustering!*
