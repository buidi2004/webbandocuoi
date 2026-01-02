#!/usr/bin/env python
"""
IVIE Wedding Studio - Script Tối Ưu Hóa và Monitoring
======================================================
Script này giúp:
- Tối ưu hóa database (indexes, vacuum, analyze)
- Monitoring hiệu suất API
- Cache management
- Health checks
- Performance benchmarking

Sử dụng:
    python optimize_admin.py --help
    python optimize_admin.py optimize-db
    python optimize_admin.py benchmark
    python optimize_admin.py health-check
    python optimize_admin.py cache-stats
"""

import argparse
import json
import os
import sys
import time
from concurrent.futures import ThreadPoolExecutor, as_completed
from datetime import datetime
from typing import Any, Dict, List, Optional, Tuple

import requests

# =============================================================================
# CONFIGURATION
# =============================================================================

DEFAULT_API_URL = os.getenv("API_BASE_URL", "http://localhost:8000")
ADMIN_API_URL = os.getenv("ADMIN_API_URL", "http://localhost:8501")

# Benchmark configuration
BENCHMARK_ENDPOINTS = [
    "/api/san_pham/",
    "/api/banner/",
    "/api/thu_vien/",
    "/api/blog/",
    "/api/thong_ke/tong_quan",
]

BENCHMARK_ITERATIONS = 10
BENCHMARK_CONCURRENCY = 5


# Colors for terminal output
class Colors:
    HEADER = "\033[95m"
    BLUE = "\033[94m"
    CYAN = "\033[96m"
    GREEN = "\033[92m"
    WARNING = "\033[93m"
    FAIL = "\033[91m"
    ENDC = "\033[0m"
    BOLD = "\033[1m"


def print_header(text: str):
    """Print formatted header"""
    print(f"\n{Colors.HEADER}{Colors.BOLD}{'=' * 60}{Colors.ENDC}")
    print(f"{Colors.HEADER}{Colors.BOLD}{text:^60}{Colors.ENDC}")
    print(f"{Colors.HEADER}{Colors.BOLD}{'=' * 60}{Colors.ENDC}\n")


def print_success(text: str):
    """Print success message"""
    print(f"{Colors.GREEN}✅ {text}{Colors.ENDC}")


def print_error(text: str):
    """Print error message"""
    print(f"{Colors.FAIL}❌ {text}{Colors.ENDC}")


def print_warning(text: str):
    """Print warning message"""
    print(f"{Colors.WARNING}⚠️  {text}{Colors.ENDC}")


def print_info(text: str):
    """Print info message"""
    print(f"{Colors.CYAN}ℹ️  {text}{Colors.ENDC}")


# =============================================================================
# API UTILITIES
# =============================================================================


def api_request(
    endpoint: str,
    method: str = "GET",
    data: dict = None,
    timeout: int = 10,
    base_url: str = None,
) -> Tuple[Optional[Any], Optional[str], float]:
    """
    Make API request and return (data, error, response_time)
    """
    url = f"{base_url or DEFAULT_API_URL}{endpoint}"
    start_time = time.time()

    try:
        if method == "GET":
            response = requests.get(url, timeout=timeout)
        elif method == "POST":
            response = requests.post(url, json=data, timeout=timeout)
        else:
            return None, f"Unsupported method: {method}", 0

        response_time = time.time() - start_time

        if response.status_code >= 400:
            return None, f"HTTP {response.status_code}", response_time

        return response.json(), None, response_time

    except requests.exceptions.Timeout:
        return None, "Timeout", time.time() - start_time
    except requests.exceptions.RequestException as e:
        return None, str(e), time.time() - start_time


# =============================================================================
# HEALTH CHECK
# =============================================================================


def health_check(api_url: str = None) -> Dict[str, Any]:
    """
    Comprehensive health check of all services
    """
    print_header("HEALTH CHECK")

    results = {
        "timestamp": datetime.now().isoformat(),
        "api_url": api_url or DEFAULT_API_URL,
        "services": {},
        "overall_status": "healthy",
    }

    # Check API server
    print_info("Checking API server...")
    data, error, response_time = api_request("/api/health", base_url=api_url)

    if error:
        results["services"]["api"] = {
            "status": "unhealthy",
            "error": error,
            "response_time": f"{response_time:.3f}s",
        }
        results["overall_status"] = "unhealthy"
        print_error(f"API server: {error}")
    else:
        results["services"]["api"] = {
            "status": "healthy",
            "data": data,
            "response_time": f"{response_time:.3f}s",
        }
        print_success(f"API server: OK ({response_time:.3f}s)")

    # Check database
    print_info("Checking database...")
    data, error, response_time = api_request("/api/db-test", base_url=api_url)

    if error:
        results["services"]["database"] = {"status": "unhealthy", "error": error}
        results["overall_status"] = "unhealthy"
        print_error(f"Database: {error}")
    else:
        results["services"]["database"] = {
            "status": "healthy",
            "data": data,
            "response_time": f"{response_time:.3f}s",
        }
        print_success(f"Database: OK ({response_time:.3f}s)")

    # Check cache
    print_info("Checking cache...")
    data, error, response_time = api_request("/api/cache/stats", base_url=api_url)

    if error:
        results["services"]["cache"] = {
            "status": "not_configured",
            "note": "Cache endpoint not available",
        }
        print_warning("Cache: Not configured or endpoint not available")
    else:
        results["services"]["cache"] = {
            "status": "healthy",
            "data": data,
            "response_time": f"{response_time:.3f}s",
        }
        print_success(f"Cache: OK ({response_time:.3f}s)")

    # Print summary
    print("\n" + "-" * 40)
    status_color = (
        Colors.GREEN if results["overall_status"] == "healthy" else Colors.FAIL
    )
    print(
        f"Overall Status: {status_color}{results['overall_status'].upper()}{Colors.ENDC}"
    )

    return results


# =============================================================================
# BENCHMARK
# =============================================================================


def benchmark_endpoint(
    endpoint: str, iterations: int = 10, base_url: str = None
) -> Dict[str, Any]:
    """
    Benchmark single endpoint
    """
    times = []
    errors = 0

    for _ in range(iterations):
        _, error, response_time = api_request(endpoint, base_url=base_url)
        if error:
            errors += 1
        else:
            times.append(response_time)

    if not times:
        return {"endpoint": endpoint, "status": "failed", "errors": errors}

    return {
        "endpoint": endpoint,
        "iterations": iterations,
        "errors": errors,
        "min": f"{min(times) * 1000:.2f}ms",
        "max": f"{max(times) * 1000:.2f}ms",
        "avg": f"{sum(times) / len(times) * 1000:.2f}ms",
        "p95": f"{sorted(times)[int(len(times) * 0.95)] * 1000:.2f}ms"
        if len(times) >= 20
        else "N/A",
        "success_rate": f"{(iterations - errors) / iterations * 100:.1f}%",
    }


def benchmark_concurrent(
    endpoint: str, concurrency: int = 5, total_requests: int = 50, base_url: str = None
) -> Dict[str, Any]:
    """
    Benchmark endpoint with concurrent requests
    """
    times = []
    errors = 0

    def make_request():
        _, error, response_time = api_request(endpoint, base_url=base_url)
        return error, response_time

    start_time = time.time()

    with ThreadPoolExecutor(max_workers=concurrency) as executor:
        futures = [executor.submit(make_request) for _ in range(total_requests)]

        for future in as_completed(futures):
            error, response_time = future.result()
            if error:
                errors += 1
            else:
                times.append(response_time)

    total_time = time.time() - start_time

    if not times:
        return {"endpoint": endpoint, "status": "failed", "errors": errors}

    return {
        "endpoint": endpoint,
        "concurrency": concurrency,
        "total_requests": total_requests,
        "errors": errors,
        "total_time": f"{total_time:.2f}s",
        "rps": f"{total_requests / total_time:.2f}",
        "min": f"{min(times) * 1000:.2f}ms",
        "max": f"{max(times) * 1000:.2f}ms",
        "avg": f"{sum(times) / len(times) * 1000:.2f}ms",
        "success_rate": f"{(total_requests - errors) / total_requests * 100:.1f}%",
    }


def run_benchmark(
    api_url: str = None,
    endpoints: List[str] = None,
    iterations: int = BENCHMARK_ITERATIONS,
    concurrent: bool = False,
    concurrency: int = BENCHMARK_CONCURRENCY,
) -> Dict[str, Any]:
    """
    Run full benchmark suite
    """
    print_header("PERFORMANCE BENCHMARK")

    endpoints = endpoints or BENCHMARK_ENDPOINTS
    results = {
        "timestamp": datetime.now().isoformat(),
        "api_url": api_url or DEFAULT_API_URL,
        "mode": "concurrent" if concurrent else "sequential",
        "endpoints": [],
    }

    for endpoint in endpoints:
        print_info(f"Benchmarking {endpoint}...")

        if concurrent:
            result = benchmark_concurrent(
                endpoint,
                concurrency=concurrency,
                total_requests=iterations,
                base_url=api_url,
            )
        else:
            result = benchmark_endpoint(endpoint, iterations, base_url=api_url)

        results["endpoints"].append(result)

        if result.get("status") == "failed":
            print_error(f"  {endpoint}: FAILED ({result.get('errors')} errors)")
        else:
            print_success(
                f"  {endpoint}: avg={result['avg']}, success={result['success_rate']}"
            )

    # Print summary
    print("\n" + "-" * 60)
    print(f"{Colors.BOLD}Benchmark Results Summary:{Colors.ENDC}")
    print("-" * 60)

    for result in results["endpoints"]:
        if result.get("status") != "failed":
            print(
                f"  {result['endpoint']:<30} avg: {result['avg']:<12} success: {result['success_rate']}"
            )

    return results


# =============================================================================
# CACHE MANAGEMENT
# =============================================================================


def cache_stats(api_url: str = None) -> Dict[str, Any]:
    """
    Get cache statistics
    """
    print_header("CACHE STATISTICS")

    data, error, _ = api_request("/api/cache/stats", base_url=api_url)

    if error:
        print_error(f"Could not get cache stats: {error}")
        return {"error": error}

    print(json.dumps(data, indent=2))
    return data


def cache_clear(api_url: str = None, pattern: str = None) -> bool:
    """
    Clear cache
    """
    print_header("CLEAR CACHE")

    endpoint = "/api/cache/clear"
    if pattern:
        endpoint += f"?pattern={pattern}"

    data, error, _ = api_request(endpoint, method="POST", base_url=api_url)

    if error:
        print_error(f"Could not clear cache: {error}")
        return False

    print_success(f"Cache cleared: {data}")
    return True


def cache_warmup(api_url: str = None) -> bool:
    """
    Warm up cache
    """
    print_header("CACHE WARMUP")

    data, error, _ = api_request("/api/cache/warmup", method="POST", base_url=api_url)

    if error:
        print_error(f"Could not warm up cache: {error}")
        return False

    print_success(f"Cache warmed up: {data}")
    return True


# =============================================================================
# DATABASE OPTIMIZATION
# =============================================================================


def optimize_database(api_url: str = None) -> Dict[str, Any]:
    """
    Run database optimizations
    """
    print_header("DATABASE OPTIMIZATION")

    results = {"timestamp": datetime.now().isoformat(), "optimizations": []}

    # This would need a dedicated endpoint in the API
    # For now, we'll just check the database health

    print_info("Checking database health...")
    data, error, _ = api_request("/api/db-test", base_url=api_url)

    if error:
        print_error(f"Database check failed: {error}")
        results["optimizations"].append(
            {"name": "health_check", "status": "failed", "error": error}
        )
    else:
        print_success("Database is healthy")
        results["optimizations"].append(
            {"name": "health_check", "status": "success", "data": data}
        )

    print_info("""
To manually optimize the database, run these SQL commands:

For PostgreSQL:
    VACUUM ANALYZE;
    REINDEX DATABASE your_database;

For SQLite:
    VACUUM;
    ANALYZE;

The API should handle index creation automatically on startup.
    """)

    return results


# =============================================================================
# MONITORING REPORT
# =============================================================================


def generate_report(api_url: str = None) -> Dict[str, Any]:
    """
    Generate comprehensive monitoring report
    """
    print_header("MONITORING REPORT")

    report = {
        "timestamp": datetime.now().isoformat(),
        "api_url": api_url or DEFAULT_API_URL,
    }

    # Health check
    print_info("Running health check...")
    report["health"] = health_check(api_url)

    # Benchmark
    print_info("\nRunning benchmark...")
    report["benchmark"] = run_benchmark(api_url, iterations=5)

    # Cache stats
    print_info("\nGetting cache stats...")
    report["cache"] = cache_stats(api_url)

    # Save report
    filename = f"monitoring_report_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
    with open(filename, "w", encoding="utf-8") as f:
        json.dump(report, f, indent=2, ensure_ascii=False)

    print_success(f"\nReport saved to: {filename}")

    return report


# =============================================================================
# CLI
# =============================================================================


def main():
    parser = argparse.ArgumentParser(
        description="IVIE Wedding Studio - Admin Optimization & Monitoring Tool",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  python optimize_admin.py health-check
  python optimize_admin.py benchmark --iterations 20
  python optimize_admin.py benchmark --concurrent --concurrency 10
  python optimize_admin.py cache-stats
  python optimize_admin.py cache-clear --pattern products
  python optimize_admin.py cache-warmup
  python optimize_admin.py report
        """,
    )

    parser.add_argument(
        "--api-url",
        default=DEFAULT_API_URL,
        help=f"API base URL (default: {DEFAULT_API_URL})",
    )

    subparsers = parser.add_subparsers(dest="command", help="Available commands")

    # Health check
    subparsers.add_parser("health-check", help="Check health of all services")

    # Benchmark
    bench_parser = subparsers.add_parser("benchmark", help="Run performance benchmark")
    bench_parser.add_argument(
        "--iterations",
        "-n",
        type=int,
        default=BENCHMARK_ITERATIONS,
        help=f"Number of iterations (default: {BENCHMARK_ITERATIONS})",
    )
    bench_parser.add_argument(
        "--concurrent", "-c", action="store_true", help="Run concurrent benchmark"
    )
    bench_parser.add_argument(
        "--concurrency",
        type=int,
        default=BENCHMARK_CONCURRENCY,
        help=f"Concurrency level (default: {BENCHMARK_CONCURRENCY})",
    )
    bench_parser.add_argument(
        "--endpoints", "-e", nargs="+", help="Specific endpoints to benchmark"
    )

    # Cache commands
    subparsers.add_parser("cache-stats", help="Show cache statistics")

    clear_parser = subparsers.add_parser("cache-clear", help="Clear cache")
    clear_parser.add_argument("--pattern", "-p", help="Pattern to match keys to clear")

    subparsers.add_parser("cache-warmup", help="Warm up cache")

    # Database
    subparsers.add_parser("optimize-db", help="Run database optimizations")

    # Full report
    subparsers.add_parser("report", help="Generate full monitoring report")

    args = parser.parse_args()

    if not args.command:
        parser.print_help()
        return

    # Execute command
    if args.command == "health-check":
        health_check(args.api_url)

    elif args.command == "benchmark":
        run_benchmark(
            api_url=args.api_url,
            endpoints=args.endpoints,
            iterations=args.iterations,
            concurrent=args.concurrent,
            concurrency=args.concurrency,
        )

    elif args.command == "cache-stats":
        cache_stats(args.api_url)

    elif args.command == "cache-clear":
        cache_clear(args.api_url, args.pattern)

    elif args.command == "cache-warmup":
        cache_warmup(args.api_url)

    elif args.command == "optimize-db":
        optimize_database(args.api_url)

    elif args.command == "report":
        generate_report(args.api_url)


if __name__ == "__main__":
    main()
