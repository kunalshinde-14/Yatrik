"use client";

import Link from "next/link";
import { useRouter } from "next/navigation";

export default function HomePage() {
  const router = useRouter();

  function goToProtectedPage(path) {
    const user = localStorage.getItem("user");

    if (!user) {
      router.push("/login");
      return;
    }

    router.push(path);
  }

  return (
    <main className="min-h-screen bg-gray-950 text-white">

      {/* Navbar */}
      <nav className="border-b border-gray-800 bg-gray-950">
        <div className="mx-auto flex max-w-6xl items-center justify-between px-6 py-5">

          <Link
            href="/"
            className="text-2xl font-bold tracking-wide"
          >
            YATRIK
          </Link>

          <div className="flex items-center gap-3">

            <Link
              href="/login"
              className="rounded-lg px-4 py-2 text-gray-300 hover:bg-gray-800 hover:text-white"
            >
              Login
            </Link>

            <Link
              href="/register"
              className="rounded-lg bg-blue-600 px-4 py-2 font-medium hover:bg-blue-700"
            >
              Register
            </Link>

          </div>

        </div>
      </nav>

      {/* Hero */}
      <section className="mx-auto flex min-h-[70vh] max-w-6xl items-center px-6">

        <div className="max-w-3xl">

          <p className="mb-4 text-sm font-semibold uppercase tracking-widest text-blue-400">
            Simple Railway Booking System
          </p>

          <h1 className="text-5xl font-bold leading-tight md:text-6xl">
            Your Journey,
            <span className="text-blue-500"> Simplified.</span>
          </h1>

          <p className="mt-6 max-w-2xl text-lg leading-8 text-gray-400">
            Search available trains, choose your journey,
            book your ticket, and manage your bookings with
            Yatrik.
          </p>

          <div className="mt-8 flex flex-wrap gap-4">

            {/* Protected Search Trains */}
            <button
              onClick={() => goToProtectedPage("/trains")}
              className="rounded-lg bg-blue-600 px-6 py-3 font-semibold hover:bg-blue-700"
            >
              Search Trains
            </button>

            {/* Protected My Bookings */}
            <button
              onClick={() => goToProtectedPage("/my-bookings")}
              className="rounded-lg border border-gray-700 px-6 py-3 font-semibold hover:bg-gray-800"
            >
              My Bookings
            </button>

          </div>

        </div>

      </section>

      {/* Features */}
      <section className="border-t border-gray-800 bg-gray-900">

        <div className="mx-auto max-w-6xl px-6 py-16">

          <h2 className="text-3xl font-bold">
            Everything You Need
          </h2>

          <p className="mt-2 text-gray-400">
            A simple railway ticket booking system.
          </p>

          <div className="mt-10 grid gap-5 md:grid-cols-4">

            <Feature
              title="Search Trains"
              description="Find trains between available stations."
            />

            <Feature
              title="Book Tickets"
              description="Enter passenger details and book your journey."
            />

            <Feature
              title="PNR"
              description="Get a unique PNR for every booking."
            />

            <Feature
              title="Manage Bookings"
              description="View and cancel your booked tickets."
            />

          </div>

        </div>

      </section>

      {/* Footer */}
      <footer className="border-t border-gray-800 px-6 py-6 text-center text-sm text-gray-500">
        Yatrik — DBMS College Project
      </footer>

    </main>
  );
}

function Feature({ title, description }) {
  return (
    <div className="rounded-2xl border border-gray-800 bg-gray-950 p-6">

      <h3 className="text-lg font-semibold">
        {title}
      </h3>

      <p className="mt-2 text-sm leading-6 text-gray-400">
        {description}
      </p>

    </div>
  );
}