# Comprehensive Analysis: Learned Perceptive Forward Dynamics Model for Safe and Platform-aware Robotic Navigation

## **1. Introduction**
### **Problem Statement**
Safe and efficient robotic navigation in complex, unstructured environments remains a significant challenge. Traditional methods rely on simplified dynamics models and handcrafted cost functions, which are:
- **Environment-dependent**: Require extensive tuning for each new scenario.
- **Non-generalizable**: Fail to adapt to diverse terrains or robot platforms.
- **Heuristic-driven**: Lack scalability and robustness in real-world deployments.

### **Motivation**
This paper addresses these limitations by proposing a **learned perceptive Forward Dynamics Model (FDM)** that:
- Predicts future robot states conditioned on **surrounding geometry** and **proprioceptive history**. 
- Integrates with a **zero-shot Model Predictive Path Integral (MPPI)** planner for safe, platform-aware navigation.
- Leverages **simulated and real-world data** to bridge the sim-to-real gap.

---

## **2. Methodology Deep Dive**
### **Architecture**
The FDM is a **neural network-based model** that predicts:
1. **Future robot poses** (`SE(2)`) over a 5-second horizon.
2. **Failure risk** (binary classification: collision/non-collision).

#### **Key Components**
- **Input Encoders**:
  - **Proprioceptive History**: Past states (poses, velocities, joint positions) encoded via a **GRU**. 
  - **Exteroceptive Input**: Height scans (from depth cameras) processed via **CNNs**.
- **Action Encoder**: MLP to encode velocity commands.
- **Forward Integration**: GRU predicts future states sequentially, conditioned on actions.
- **Prediction Heads**:
  - **Pose Head**: Predicts residual velocities (`Δa`) integrated into final poses.
  - **Risk Head**: Estimates failure probability via sigmoid activation.

#### **Residual Formulation**
Instead of predicting absolute poses, the model predicts **velocity corrections** (`Δa`) to improve accuracy and stability.

---

### **Training Process**
#### **Data Collection**
- **Simulated Data**:
  - Generated using **NVIDIA IsaacLab** with terrain randomization (stairs, ramps, rough ground).
  - Includes **high-risk maneuvers** (e.g., collisions) to improve failure prediction.
  - **Action Sampling**: Initially random, later guided by MPPI to align with planner behavior.
- **Real-World Data**:
  - Collected using **ANYmal** robot with **Boxi sensor payload** (depth cameras, RTK-GNSS, IMU).
  - Covers diverse terrains (pavement, snow, forests) to capture **non-rigid dynamics** (e.g., slipping, vegetation entanglement).

#### **Training Strategy**
1. **Pre-training**: Exclusively on simulated data with **augmented noise** to improve robustness.
2. **Fine-tuning**: Mixed real-world and simulated data to bridge the reality gap.
3. **Loss Function**:
   - **Pose Loss**: MSE between predicted and ground-truth poses (with sinusoidal encoding for heading).
   - **Risk Loss**: Binary cross-entropy for failure prediction.
   - **Stop Loss**: Penalizes pose deviations post-failure (MSE).

#### **Hyperparameters**
- Prediction horizon: **10 steps (5 sec)**.
- History horizon: **10 steps (0.5 sec)**.
- Optimizer: **AdamW** with learning rate scheduling.

---

### **Experimental Setup**
#### **Simulation Environments**
| Environment | Description                          | Obstacles                          |
|-------------|--------------------------------------|------------------------------------|
| **2D**      | Flat terrain with 2D obstacles       | Walls, pillars, mazes              |
| **2D-3D**   | Mixed 2D and 3D obstacles            | Stairs, ramps, walls               |
| **3D**      | Complex 3D terrain                   | Stairs, ramps, rough ground        |

#### **Real-World Tests**
- **Platform**: ANYmal quadruped robot.
- **Terrains**: Pavement, snow, forests.
- **Sensors**: Depth cameras (height scans), RTK-GNSS, IMU.

#### **Baselines**
1. **Constant Velocity Model**: Assumes no environmental interaction.
2. **Kim et al. [5]**: Perceptive FDM using **2D LiDAR** (no height scans).
3. **Heuristic Traversability [30]**: Rule-based cost maps for MPPI.

---

## **3. Experiments & Results**
### **Simulation Results**
#### **FDM Perceptiveness**
- **Qualitative**: Fig. 4 shows the model adapts predictions to terrain (e.g., stairs vs. ramps).
- **Quantitative**:
  - **Position Error**: 41% lower than Kim et al. [5], 70% lower than constant velocity (Fig. 6).
  - **Failure Prediction**: F1 score of **0.90** (2D) and **0.85** (3D) (Tab. II).

#### **Planning Performance**
| Environment | Method               | Success Rate (%) | Mean Path Length (m) | Mean Path Time (s) |
|-------------|----------------------|------------------|----------------------|--------------------|
| **2D**      | Ours                 | **88.33**        | 4.28                 | 9.23               |
|             | Kim et al. [5]       | 78.33            | 9.98                 | 25.01              |
|             | Heuristics [30]      | 82.50            | 4.73                 | 11.12              |
| **3D**      | Ours                 | **73.75**        | 3.93                 | 8.68               |
|             | Kim et al. [5]       | 48.75            | 7.20                 | 18.60              |
|             | Heuristics [30]      | 33.13            | 4.41                 | 13.99              |

**Key Insight**: The FDM enables **zero-shot adaptation** to new environments without retraining.

---

### **Real-World Results**
#### **Sim-to-Real Transfer**
- **Position Error**: Reduced by **30–34%** after fine-tuning (Fig. 8).
- **Qualitative**: Fig. 14 shows accurate predictions in snow/forests despite sensor noise.

#### **Failure Cases**
- **Limitations**:
  - **Novel Geometries**: Struggles with spiral staircases or caves.
  - **Extreme Terrain**: Ice/mud may exceed locomotion policy capabilities.
  - **False Negatives**: Rare failure predictions in high-risk scenarios.

---

## **4. Ablation Studies**
### **Critical Components**
| Component               | Impact on Position Error | Impact on F1 Score |
|-------------------------|--------------------------|--------------------|
| **Past States**         | None                     | +0.06              |
| **Proprioception**      | +800%                    | -0.20              |
| **Height Scan**         | +110%                    | -0.13              |

**Key Insight**: Exteroceptive input (height scans) is **most critical** for traversability assessment.

### **Planning Reward Terms**
- **Failure Risk Reward**: Improves success rate by **2.5–4.6%** (Tab. VI).

---

## **5. Comparison with Related Work**
| **Category**               | **Prior Work**                          | **This Work**                          | **Improvements**                          |
|----------------------------|-----------------------------------------|----------------------------------------|-------------------------------------------|
| **Learned Dynamics**       | Kim et al. [5] (2D LiDAR)               | **Perceptive FDM (Height Scans)**      | +41% position accuracy, 3D generalization |
| **Zero-Shot Planners**     | MPPI with heuristic costs [30]          | **FDM + Simplified MPPI**              | No cost tuning, 27% higher success rate   |
| **Sim-to-Real Transfer**   | Domain randomization [40]               | **Hybrid sim/real training**           | 30% lower real-world error                |

---

## **6. Limitations & Failure Cases**
### **Limitations**
1. **Geometric Domain**: Assumes terrain variations are covered during training.
2. **Failure Mismatch**: Simulated failures ≠ real-world failures (e.g., no hardware damage in sim).
3. **Social Norms**: Ignores dynamic agents (e.g., pedestrians).
4. **Parameter Sensitivity**: MPPI requires tuning for action distributions.

### **Failure Cases**
- **False Negatives**: Rarely misses collisions in cluttered environments.
- **Out-of-Distribution Terrain**: Fails on ice/mud or novel geometries (e.g., caves).
- **Sensor Noise**: Real-world depth cameras may introduce occlusions.

---

## **7. Future Directions**
1. **Adaptive Timesteps**: Dynamically adjust prediction horizons.
2. **RGB Input**: Replace height scans with richer visual features.
3. **Uncertainty Estimation**: Use ensemble learning for risk-aware planning.
4. **Multi-Robot Systems**: Extend to collaborative navigation.
5. **Physics Simulator Fidelity**: Improve simulation of soft/non-rigid terrains.

---

## **8. Conclusion**
### **Summary of Impact**
- **First** perceptive FDM for **rough-terrain quadruped navigation**. 
- **41% lower position error** and **27% higher success rate** vs. baselines.
- **Zero-shot adaptation** to new environments via simplified MPPI rewards.
- **Sim-to-real transfer** enabled by hybrid training.

### **Broader Implications**
- **Reduces reliance on handcrafted cost functions** for safe navigation.
- **Platform-aware predictions** generalize across legged/wheeled robots.
- **Paves the way** for learned dynamics in high-speed off-road autonomy.

---

## **9. Supplementary Materials**
- **Code**: [GitHub - LeggedRobotics/FDM](https://github.com/leggedrobotics/fdm)
- **Datasets**: Simulated (IsaacLab) and real-world (ANYmal deployments).
- **Video Demos**: [RSS 2025 Presentation](https://youtu.be/example) (hypothetical link).