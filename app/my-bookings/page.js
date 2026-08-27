"use client";

import { useEffect, useState } from "react";

export default function MyBookingsPage() {
  const [bookings, setBookings] = useState([]);
  const [loading, setLoading] = useState(true);
  const [cancelLoading, setCancelLoading] = useState(null);
  const [message, setMessage] = useState("");

  useEffect(() => {
    loadBookings();
  }, []);

  async function loadBookings() {
    try {
      const userData = localStorage.getItem("user");

      if (!userData) {
        setMessage("Please login to view your bookings.");
        setLoading(false);
        return;
      }

      const user = JSON.parse(userData);

      const response = await fetch(
        `/api/my-bookings?userId=${user.USER_ID}`
      );

      const data = await response.json();

      if (data.success) {
        setBookings(data.data);

        if (data.data.length === 0) {
          setMessage("You have no bookings yet.");
        }
      } else {
        setMessage(data.message);
      }
    } catch (error) {
      console.error(error);
      setMessage("Unable to load bookings.");
    } finally {
      setLoading(false);
    }
  }

  function formatDate(dateString) {
    const date = new Date(dateString);

    return date.toLocaleDateString("en-IN", {
      day: "2-digit",
      month: "short",
      year: "numeric",
    });
  }

  async function cancelBooking(bookingId) {
    const userData = localStorage.getItem("user");

    if (!userData) {
      setMessage("Please login again.");
      return;
    }

    const user = JSON.parse(userData);

    const confirmed = window.confirm(
      "Are you sure you want to cancel this ticket?"
    );

    if (!confirmed) {
      return;
    }

    setCancelLoading(bookingId);
    setMessage("");

    try {
      const response = await fetch("/api/cancel-booking", {
        method: "PUT",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify({
          bookingId,
          userId: user.USER_ID,
        }),
      });

      const data = await response.json();

      if (data.success) {
        setMessage("Booking cancelled successfully.");

        // Refresh bookings
        await loadBookings();
      } else {
        setMessage(data.message);
      }
    } catch (error) {
      console.error(error);
      setMessage("Unable to cancel booking.");
    } finally {
      setCancelLoading(null);
    }
  }

  return (
    <main className="min-h-screen bg-gray-950 px-6 py-10 text-white">
      <div className="mx-auto max-w-5xl">

        {/* Heading */}

        <h1 className="text-4xl font-bold">
          My Bookings
        </h1>

        <p className="mt-2 text-gray-400">
          View and manage your booked train tickets
        </p>

        {/* Message */}

        {message && (
          <div className="mt-6 rounded-lg border border-gray-800 bg-gray-900 p-4 text-center text-gray-300">
            {message}
          </div>
        )}

        {/* Loading */}

        {loading && (
          <p className="mt-10 text-center text-gray-400">
            Loading bookings...
          </p>
        )}

        {/* No bookings */}

        {!loading &&
          bookings.length === 0 &&
          !message && (
            <div className="mt-10 rounded-2xl border border-gray-800 bg-gray-900 p-8 text-center">
              <p className="text-gray-400">
                You have no bookings yet.
              </p>
            </div>
          )}

        {/* Booking Cards */}

        {!loading && bookings.length > 0 && (
          <div className="mt-8 space-y-6">

            {bookings.map((booking) => (
              <div
                key={booking.BOOKING_ID}
                className="rounded-2xl border border-gray-800 bg-gray-900 p-6"
              >

                {/* Header */}

                <div className="flex flex-col justify-between gap-4 md:flex-row md:items-center">

                  <div>
                    <p className="text-sm text-gray-500">
                      PNR
                    </p>

                    <p className="text-xl font-bold text-blue-400">
                      {booking.PNR}
                    </p>
                  </div>

                  <span
                    className={`w-fit rounded-full px-4 py-1 text-sm font-medium ${
                      booking.STATUS === "CONFIRMED"
                        ? "bg-green-900 text-green-400"
                        : "bg-red-900 text-red-400"
                    }`}
                  >
                    {booking.STATUS}
                  </span>

                </div>

                <div className="my-6 border-t border-gray-800" />

                {/* Train */}

                <div>
                  <p className="text-sm text-gray-500">
                    {booking.TRAIN_NUMBER}
                  </p>

                  <h2 className="mt-1 text-2xl font-bold">
                    {booking.TRAIN_NAME}
                  </h2>

                  <p className="mt-2 text-gray-400">
                    {booking.SOURCE} → {booking.DESTINATION}
                  </p>
                </div>

                {/* Details */}

                <div className="mt-6 grid gap-5 sm:grid-cols-2 md:grid-cols-4">

                  <div>
                    <p className="text-sm text-gray-500">
                      Passenger
                    </p>

                    <p className="mt-1 font-medium">
                      {booking.PASSENGER_NAME}
                    </p>
                  </div>

                  <div>
                    <p className="text-sm text-gray-500">
                      Age
                    </p>

                    <p className="mt-1 font-medium">
                      {booking.AGE}
                    </p>
                  </div>

                  <div>
                    <p className="text-sm text-gray-500">
                      Gender
                    </p>

                    <p className="mt-1 font-medium">
                      {booking.GENDER}
                    </p>
                  </div>

                  <div>
                    <p className="text-sm text-gray-500">
                      Journey Date
                    </p>

                    <p className="mt-1 font-medium">
                      {formatDate(booking.JOURNEY_DATE)}
                    </p>
                  </div>

                </div>

                {/* Bottom */}

                <div className="mt-6 flex flex-col gap-4 border-t border-gray-800 pt-5 sm:flex-row sm:items-center sm:justify-between">

                  <div>
                    <span className="text-gray-400">
                      Fare
                    </span>

                    <span className="ml-3 text-xl font-bold">
                      ₹{booking.FARE}
                    </span>
                  </div>

                  {/* Cancel Button */}

                  {booking.STATUS === "CONFIRMED" && (
                    <button
                      onClick={() =>
                        cancelBooking(booking.BOOKING_ID)
                      }
                      disabled={cancelLoading === booking.BOOKING_ID}
                      className="rounded-lg bg-red-600 px-5 py-3 font-semibold hover:bg-red-700 disabled:cursor-not-allowed disabled:opacity-50"
                    >
                      {cancelLoading === booking.BOOKING_ID
                        ? "Cancelling..."
                        : "Cancel Ticket"}
                    </button>
                  )}

                </div>

              </div>
            ))}

          </div>
        )}

      </div>
    </main>
  );
}