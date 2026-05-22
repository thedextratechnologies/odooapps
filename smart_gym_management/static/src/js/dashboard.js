/** @odoo-module **/

import { registry } from "@web/core/registry";
import { Component, onMounted, onWillStart, useRef, useState } from "@odoo/owl";
import { useService } from "@web/core/utils/hooks";

class GymDashboard extends Component {

    setup() {

        this.orm = useService("orm");

        this.memberChart = useRef("memberChart");
        this.paymentChart = useRef("paymentChart");

        this.state = useState({

            total_members: 0,
            active_members: 0,
            inactive_members: 0,

            total_trainers: 0,
            total_workouts: 0,
            total_plans: 0,
            total_equipments: 0,

            fully_paid_members: 0,
            partially_paid_members: 0,
        });

        onWillStart(async () => {

            // MEMBERS

            this.state.total_members = await this.orm.searchCount(
                "gym.member", []
            );

            this.state.active_members = await this.orm.searchCount(
                "gym.member",
                [['member_status', '=', 'active']]
            );

            this.state.inactive_members = await this.orm.searchCount(
                "gym.member",
                [['member_status', '=', 'inactive']]
            );

            // TRAINERS

            this.state.total_trainers = await this.orm.searchCount(
                "gym.trainer", []
            );

            // WORKOUTS

            this.state.total_workouts = await this.orm.searchCount(
                "gym.workout", []
            );

            // MEMBERSHIP PLANS

            this.state.total_plans = await this.orm.searchCount(
                "gym.membership", []
            );

            // EQUIPMENTS

            this.state.total_equipments = await this.orm.searchCount(
                "product.template",
                [["is_gym_equipment", "=", true]]
            );

            // FULLY PAID

            this.state.fully_paid_members = await this.orm.searchCount(
                "account.move",
                [
                    ["move_type", "=", "out_invoice"],
                    ["payment_state", "=", "paid"]
                ]
            );

            // PARTIALLY PAID

            this.state.partially_paid_members = await this.orm.searchCount(
                "account.move",
                [
                    ["move_type", "=", "out_invoice"],
                    ["payment_state", "=", "partial"]
                ]
            );
        });

        onMounted(() => {
            this.renderCharts();
        });
    }

    renderCharts() {

        // MEMBER CHART

        new Chart(this.memberChart.el, {

            type: 'bar',

            data: {

                labels: [
                    'Total',
                    'Active',
                    'Inactive'
                ],

                datasets: [{

                    label: 'Members',

                    data: [
                        this.state.total_members,
                        this.state.active_members,
                        this.state.inactive_members
                    ],

                    backgroundColor: [
                        '#7c3aed',
                        '#22c55e',
                        '#ef4444'
                    ],

                    borderRadius: 8,
                    barThickness: 40,
                }]
            },

            options: {

                responsive: true,
                maintainAspectRatio: false,

                plugins: {
                    legend: {
                        display: false
                    }
                },

                scales: {
                    y: {
                        beginAtZero: true
                    }
                }
            }
        });

        // PAYMENT CHART

        new Chart(this.paymentChart.el, {

            type: 'doughnut',

            data: {

                labels: [
                    'Fully Paid',
                    'Partially Paid'
                ],

                datasets: [{

                    data: [
                        this.state.fully_paid_members,
                        this.state.partially_paid_members
                    ],

                    backgroundColor: [
                        '#22c55e',
                        '#f59e0b'
                    ],
                }]
            },

            options: {

                responsive: true,
                maintainAspectRatio: false,
                cutout: '65%',
            }
        });
    }
}

GymDashboard.template = "gym_management_system.GymDashboard";

registry.category("actions").add("gym_dashboard_tag", GymDashboard);