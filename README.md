# Comparative-analysis-of-Koopman-Kalman-filter-and-EKF

## Summary
In this we compare a new filter designed based on operator theoretic framework of dynamical systems with a widely used variant of the Kalman Filter. Specifically, we use Koopman operator theory to derive a high-dimensional embedding of the nonlinear dynamics in which the system outputs evolve in a linear fashion. We see that by exploiting this linear structure of the Koopman operator,we can design linear observers like Kalman Filter for nonlinear state estimation.We compare the performance of this Koopman Kalman Filter with Extended
Kalman Filter and observe that KKF shows superior performance. This is attributed to the fact that EKF performs a local linearization of the system while Koopman theory facilitates (nearly) global linearization of nonlinear dynamics.

## Koopman Operator Theory
The system identification method exploits the fact that any finite-dimensional nonlinear system can be equivalently represented using an infinite-dimensional linear system by transforming the traditional state-space to the space of functions (observables) of the system's states and inputs.

## System identification using EDMD
The Koopman operator theory is conceptually developed on the infinite-dimensional function space G. However, it is not practically feasible unless we can determine finite-dimensional approximations to the Koopman operator without a great loss in accuracy.

## Koopman model validation
The following figure shows the output predictions of the above determined Koopman linear model for two different inputs (randomly) chosen for the linear and angular velocities. From the figure it can be seen that the true model and the identified linear model is overlapping in both the cases resulting in a very good accuracy. This is expected because the derived linearization is exact (not approximate) and is therefore valid globally.

![]()

## State Estimation
Now that the Koopman model has been validated, we used the linear model to perform state estimation using a Kalman Filter as described in the previous section. In order to evaluate the performance of the Koopman based Filter KKF, we compared its estimation performance with the commonly used EKF.We considered two cases: (a) v/w = 10 and (b)v/w = 100. Figure shows the estimation results of KKF and EKF respectively for Case (a) and Figure shows the estimation results of KKF and EKF respectively for Case (b). From the figures, we can see that in Case (a) the KKF performs slightly better than EKF, however, in Case (b) the performance of both the filters is comparative. Figures show the averaged root mean squared error for both the cases for EKF and KKF respectively.

## Conclusions
Koopman operator theory offers a new direction in state estimation theory. Specifically, it facilitates linear observer design for nonlinear state estimation. The idea is to obtian a Koopman linear model for the underlying nonlinear system and then design any linear filters available to perform the estimation. In the example considered in this project we obtained an exact linearization of the original system which makes the Koopman model valid globally. Because it is a global linearization it is expected to perform better than EKF. However, due to the approximation present in liftng the initial distribution where we assume Gaussian even for the lifted variable (this is clearly not valid as we perform a nonlinear transformation) the performance is comparable if not better in the case of KKF. However, in future it will be interesting to study KKF for more complex systems where EKF fails. Additionally, it will be of interest to study the performance when the frequency of measurements is lower than what was considered in this project because it is well known that EKF performance degrades with a lower rate of measurements.

