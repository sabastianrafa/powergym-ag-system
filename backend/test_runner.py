#!/usr/bin/env python3
"""
Automated API Testing Utility Script
Tests all endpoints sequentially with colored console output
"""

import requests
import sys
from datetime import datetime
from typing import Dict, List, Tuple
import json


class Colors:
    """ANSI color codes for terminal output."""
    GREEN = '\033[92m'
    RED = '\033[91m'
    YELLOW = '\033[93m'
    BLUE = '\033[94m'
    MAGENTA = '\033[95m'
    CYAN = '\033[96m'
    RESET = '\033[0m'
    BOLD = '\033[1m'


class APITester:
    """Automated API testing utility."""

    def __init__(self, base_url: str = "http://localhost:8000"):
        self.base_url = base_url
        self.access_token = None
        self.results: List[Tuple[str, bool, str]] = []
        self.test_customer_id = None
        self.test_biometric_id = None

    def print_header(self, text: str):
        """Print a formatted header."""
        print(f"\n{Colors.BOLD}{Colors.CYAN}{'=' * 70}{Colors.RESET}")
        print(f"{Colors.BOLD}{Colors.CYAN}{text.center(70)}{Colors.RESET}")
        print(f"{Colors.BOLD}{Colors.CYAN}{'=' * 70}{Colors.RESET}\n")

    def print_test(self, name: str, passed: bool, message: str = ""):
        """Print test result with color."""
        status = f"{Colors.GREEN}PASS{Colors.RESET}" if passed else f"{Colors.RED}FAIL{Colors.RESET}"
        print(f"[{status}] {name}")
        if message:
            color = Colors.GREEN if passed else Colors.RED
            print(f"      {color}{message}{Colors.RESET}")
        self.results.append((name, passed, message))

    def print_section(self, text: str):
        """Print a section header."""
        print(f"\n{Colors.BOLD}{Colors.MAGENTA}>>> {text}{Colors.RESET}")

    def test_auth(self) -> bool:
        """Test authentication endpoints."""
        self.print_section("Testing Authentication")

        try:
            response = requests.post(
                f"{self.base_url}/auth/login",
                data={
                    "username": "admin@gym.com",
                    "password": "admin123"
                }
            )

            if response.status_code == 200:
                data = response.json()
                self.access_token = data.get("access_token")
                self.print_test("Login with valid credentials", True, f"Token obtained")
                return True
            else:
                self.print_test("Login with valid credentials", False, f"Status: {response.status_code}")
                return False

        except Exception as e:
            self.print_test("Login with valid credentials", False, str(e))
            return False

    def test_invalid_login(self):
        """Test login with invalid credentials."""
        try:
            response = requests.post(
                f"{self.base_url}/auth/login",
                data={
                    "username": "invalid@test.com",
                    "password": "wrongpassword"
                }
            )

            passed = response.status_code == 401
            self.print_test("Login with invalid credentials", passed, f"Status: {response.status_code}")

        except Exception as e:
            self.print_test("Login with invalid credentials", False, str(e))

    def test_protected_endpoint(self):
        """Test accessing protected endpoint."""
        try:
            headers = {"Authorization": f"Bearer {self.access_token}"}
            response = requests.get(f"{self.base_url}/protected", headers=headers)

            passed = response.status_code == 200
            self.print_test("Access protected endpoint", passed, f"Status: {response.status_code}")

        except Exception as e:
            self.print_test("Access protected endpoint", False, str(e))

    def test_list_customers(self):
        """Test listing customers."""
        self.print_section("Testing Customer Endpoints")

        try:
            headers = {"Authorization": f"Bearer {self.access_token}"}
            response = requests.get(f"{self.base_url}/customers", headers=headers)

            passed = response.status_code == 200
            count = len(response.json()) if passed else 0
            self.print_test("List all customers", passed, f"Found {count} customers")

        except Exception as e:
            self.print_test("List all customers", False, str(e))

    def test_create_customer(self) -> bool:
        """Test creating a customer."""
        try:
            headers = {
                "Authorization": f"Bearer {self.access_token}",
                "Content-Type": "application/json"
            }

            customer_data = {
                "dni": f"TEST{datetime.now().strftime('%Y%m%d%H%M%S')}",
                "first_name": "Test",
                "last_name": "Customer",
                "birth_date": "1990-01-15",
                "gender": "male",
                "email": f"test.{datetime.now().strftime('%Y%m%d%H%M%S')}@test.com",
                "phone": "+1234567890",
                "address": "123 Test Street",
                "emergency_contact_name": "Emergency Contact",
                "emergency_contact_phone": "+0987654321",
                "status": "active"
            }

            response = requests.post(
                f"{self.base_url}/customers",
                headers=headers,
                json=customer_data
            )

            if response.status_code == 201:
                data = response.json()
                self.test_customer_id = data.get("id")
                self.print_test("Create customer", True, f"Customer ID: {self.test_customer_id}")
                return True
            else:
                self.print_test("Create customer", False, f"Status: {response.status_code} - {response.text}")
                return False

        except Exception as e:
            self.print_test("Create customer", False, str(e))
            return False

    def test_get_customer(self):
        """Test retrieving a customer by ID."""
        if not self.test_customer_id:
            self.print_test("Get customer by ID", False, "No test customer ID available")
            return

        try:
            headers = {"Authorization": f"Bearer {self.access_token}"}
            response = requests.get(
                f"{self.base_url}/customers/{self.test_customer_id}",
                headers=headers
            )

            passed = response.status_code == 200
            self.print_test("Get customer by ID", passed, f"Status: {response.status_code}")

        except Exception as e:
            self.print_test("Get customer by ID", False, str(e))

    def test_update_customer(self):
        """Test updating a customer."""
        if not self.test_customer_id:
            self.print_test("Update customer", False, "No test customer ID available")
            return

        try:
            headers = {
                "Authorization": f"Bearer {self.access_token}",
                "Content-Type": "application/json"
            }

            update_data = {
                "phone": "+9999999999",
                "address": "456 Updated Street"
            }

            response = requests.put(
                f"{self.base_url}/customers/{self.test_customer_id}",
                headers=headers,
                json=update_data
            )

            passed = response.status_code == 200
            self.print_test("Update customer", passed, f"Status: {response.status_code}")

        except Exception as e:
            self.print_test("Update customer", False, str(e))

    def test_search_customers(self):
        """Test searching customers."""
        try:
            headers = {"Authorization": f"Bearer {self.access_token}"}
            response = requests.get(
                f"{self.base_url}/customers/search?query=Test",
                headers=headers
            )

            passed = response.status_code == 200
            count = len(response.json()) if passed else 0
            self.print_test("Search customers", passed, f"Found {count} results")

        except Exception as e:
            self.print_test("Search customers", False, str(e))

    def test_list_biometrics(self):
        """Test listing biometrics."""
        self.print_section("Testing Biometric Endpoints")

        try:
            headers = {"Authorization": f"Bearer {self.access_token}"}
            response = requests.get(f"{self.base_url}/biometrics", headers=headers)

            passed = response.status_code == 200
            count = len(response.json()) if passed else 0
            self.print_test("List all biometrics", passed, f"Found {count} biometrics")

        except Exception as e:
            self.print_test("List all biometrics", False, str(e))

    def test_list_subscriptions(self):
        """Test listing subscriptions."""
        self.print_section("Testing Subscription Endpoints")

        try:
            headers = {"Authorization": f"Bearer {self.access_token}"}
            response = requests.get(f"{self.base_url}/subscriptions", headers=headers)

            passed = response.status_code == 200
            count = len(response.json()) if passed else 0
            self.print_test("List all subscriptions", passed, f"Found {count} subscriptions")

        except Exception as e:
            self.print_test("List all subscriptions", False, str(e))

    def test_list_payments(self):
        """Test listing payments."""
        self.print_section("Testing Payment Endpoints")

        try:
            headers = {"Authorization": f"Bearer {self.access_token}"}
            response = requests.get(f"{self.base_url}/payments", headers=headers)

            passed = response.status_code == 200
            count = len(response.json()) if passed else 0
            self.print_test("List all payments", passed, f"Found {count} payments")

        except Exception as e:
            self.print_test("List all payments", False, str(e))

    def test_list_attendances(self):
        """Test listing attendances."""
        self.print_section("Testing Attendance Endpoints")

        try:
            headers = {"Authorization": f"Bearer {self.access_token}"}
            response = requests.get(f"{self.base_url}/attendances", headers=headers)

            passed = response.status_code == 200
            count = len(response.json()) if passed else 0
            self.print_test("List all attendances", passed, f"Found {count} attendances")

        except Exception as e:
            self.print_test("List all attendances", False, str(e))

    def test_today_attendances(self):
        """Test getting today's attendances."""
        try:
            headers = {"Authorization": f"Bearer {self.access_token}"}
            response = requests.get(f"{self.base_url}/attendances/today", headers=headers)

            passed = response.status_code == 200
            count = len(response.json()) if passed else 0
            self.print_test("Get today's attendances", passed, f"Found {count} attendances today")

        except Exception as e:
            self.print_test("Get today's attendances", False, str(e))

    def test_delete_customer(self):
        """Test deleting a customer (soft delete)."""
        if not self.test_customer_id:
            self.print_test("Delete customer", False, "No test customer ID available")
            return

        try:
            headers = {"Authorization": f"Bearer {self.access_token}"}
            response = requests.delete(
                f"{self.base_url}/customers/{self.test_customer_id}",
                headers=headers
            )

            passed = response.status_code == 204
            self.print_test("Delete customer (soft delete)", passed, f"Status: {response.status_code}")

        except Exception as e:
            self.print_test("Delete customer (soft delete)", False, str(e))

    def print_summary(self):
        """Print test summary."""
        self.print_header("TEST SUMMARY")

        total = len(self.results)
        passed = sum(1 for _, p, _ in self.results if p)
        failed = total - passed
        success_rate = (passed / total * 100) if total > 0 else 0

        print(f"{Colors.BOLD}Total Tests:{Colors.RESET} {total}")
        print(f"{Colors.GREEN}{Colors.BOLD}Passed:{Colors.RESET} {passed}")
        print(f"{Colors.RED}{Colors.BOLD}Failed:{Colors.RESET} {failed}")
        print(f"{Colors.BOLD}Success Rate:{Colors.RESET} {success_rate:.1f}%\n")

        if failed > 0:
            print(f"{Colors.RED}{Colors.BOLD}Failed Tests:{Colors.RESET}")
            for name, passed, message in self.results:
                if not passed:
                    print(f"  - {name}: {message}")
            print()

    def run_all_tests(self):
        """Run all tests sequentially."""
        self.print_header("GYM MANAGEMENT SYSTEM API TESTER")
        print(f"{Colors.BOLD}Base URL:{Colors.RESET} {self.base_url}")
        print(f"{Colors.BOLD}Date:{Colors.RESET} {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")

        if not self.test_auth():
            print(f"\n{Colors.RED}{Colors.BOLD}Authentication failed. Cannot continue tests.{Colors.RESET}\n")
            return

        self.test_invalid_login()
        self.test_protected_endpoint()

        self.test_list_customers()
        if self.test_create_customer():
            self.test_get_customer()
            self.test_update_customer()
        self.test_search_customers()

        self.test_list_biometrics()
        self.test_list_subscriptions()
        self.test_list_payments()
        self.test_list_attendances()
        self.test_today_attendances()

        self.test_delete_customer()

        self.print_summary()


def main():
    """Main function."""
    base_url = "http://localhost:8000"

    if len(sys.argv) > 1:
        base_url = sys.argv[1]

    tester = APITester(base_url)

    try:
        tester.run_all_tests()
    except KeyboardInterrupt:
        print(f"\n\n{Colors.YELLOW}Tests interrupted by user.{Colors.RESET}\n")
        tester.print_summary()
        sys.exit(1)
    except Exception as e:
        print(f"\n\n{Colors.RED}Error running tests: {e}{Colors.RESET}\n")
        sys.exit(1)


if __name__ == "__main__":
    main()
