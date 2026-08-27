"use client";

import { useEffect, useState } from "react";

export default function TrainsPage() {
  const [stations, setStations] = useState([]);
  const [trains, setTrains] = useState([]);

  const [source, setSource] = useState("");
  const [destination, setDestination] = useState("");

  const [selectedTrain, setSelectedTrain] = useState(null);

  const [passengerName, setPassengerName] = useState("");
  const [age, setAge] = useState("");
  const [gender, setGender] = useState("");
  const [journeyDate, setJourneyDate] = useState("");

  const [loading, setLoading] = useState(true);
  const [bookingLoading, setBookingLoading] = useState(false);
  const [message, setMessage] = useState("");
  const [bookingSuccess, setBookingSuccess] = useState(null);

  useEffect(() => {
    loadData();
  }, []);

  async function loadData() {
    try {
      const [stationResponse, trainResponse] = await Promise.all([
        fetch("/api/stations"),
        fetch("/api/trains"),
      ]);

      const stationData = await stationResponse.json();
      const trainData = await trainResponse.json();

      if (stationData.success) {
        setStations(stationData.data);
      }

      if (trainData.success) {
        setTrains(trainData.data);
      }
    } catch (error) {
      console.error(error);
      setMessage("Unable to load data.");
    } finally {
      setLoading(false);
    }
  }

  async function searchTrains(e) {
    e.preventDefault();

    if (!source || !destination) {
      setMessage("Please select both stations.");
      return;
    }

    if (source === destination) {
      setMessage("From and To stations cannot be the same.");
      return;
    }

    setLoading(true);
    setMessage("");

    try {
      const response = await fetch(
        `/api/trains?source=${encodeURIComponent(
          source
        )}&destination=${encodeURIComponent(destination)}`
      );

      const data = await response.json();

      if (data.success) {
        setTrains(data.data);

        if (data.data.length === 0) {
          setMessage("No trains found for this route.");
        }
      } else {
        setMessage(data.message);
      }
    } catch (error) {
      console.error(error);
      setMessage("Unable to search trains.");
    } finally {
      setLoading(false);
    }
  }

  async function showAllTrains() {
    setSource("");
    setDestination("");
    setMessage("");
    setLoading(true);

    try {
      const response = await fetch("/api/trains");
      const data = await response.json();

      if (data.success) {
        setTrains(data.data);
      }
    } catch (error) {
      console.error(error);
      setMessage("Unable to load trains.");
    } finally {
      setLoading(false);
    }
  }

  function openBooking(train) {
    const user = localStorage.getItem("user");

    if (!user) {
      setMessage("Please login before booking a ticket.");
      return;
    }

    setSelectedTrain(train);
    setPassengerName("");
    setAge("");
    setGender("");
    setJourneyDate("");
    setBookingSuccess(null);
    setMessage("");
  }

  async function handleBooking(e) {
    e.preventDefault();

    const user = JSON.parse(localStorage.getItem("user"));

    if (!user) {
      setMessage("Please login before booking.");
      return;
    }

    if (!selectedTrain) {
      return;
    }

    setBookingLoading(true);
    setMessage("");

    try {
      const response = await fetch("/api/bookings", {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify({
          userId: user.USER_ID,
          trainId: selectedTrain.TRAIN_ID,
          passengerName,
          age: Number(age),
          gender,
          journeyDate,
        }),
      });

      const data = await response.json();

      if (data.success) {
        setBookingSuccess(data);
        setSelectedTrain(null);
      } else {
        setMessage(data.message);
      }
    } catch (error) {
      console.error(error);
      setMessage("Unable to book ticket.");
    } finally {
      setBookingLoading(false);
    }
  }

  return (
    <main className="min-h-screen bg-gray-950 px-6 py-10 text-white">
      <div className="mx-auto max-w-6xl">

        {/* Page Heading */}
        <h1 className="text-4xl font-bold">
          Search Trains
        </h1>

        <p className="mt-2 text-gray-400">
          Find trains for your journey
        </p>

        {/* ================= SEARCH FORM ================= */}

        <form
          onSubmit={searchTrains}
          className="mt-8 grid gap-4 rounded-2xl bg-gray-900 p-6 md:grid-cols-3"
        >

          {/* From */}
          <div>
            <label className="mb-2 block text-sm font-medium text-gray-300">
              From
            </label>

            <select
              value={source}
              onChange={(e) => setSource(e.target.value)}
              className="w-full rounded-lg border border-gray-700 bg-gray-800 px-4 py-3 text-white outline-none focus:border-blue-500"
            >
              <option value="">
                Select departure station
              </option>

              {stations.map((station) => (
                <option
                  key={station.STATION_ID}
                  value={station.STATION_NAME}
                >
                  {station.STATION_NAME}
                </option>
              ))}
            </select>
          </div>

          {/* To */}
          <div>
            <label className="mb-2 block text-sm font-medium text-gray-300">
              To
            </label>

            <select
              value={destination}
              onChange={(e) => setDestination(e.target.value)}
              className="w-full rounded-lg border border-gray-700 bg-gray-800 px-4 py-3 text-white outline-none focus:border-blue-500"
            >
              <option value="">
                Select arrival station
              </option>

              {stations.map((station) => (
                <option
                  key={station.STATION_ID}
                  value={station.STATION_NAME}
                >
                  {station.STATION_NAME}
                </option>
              ))}
            </select>
          </div>

          {/* Search Button */}
          <div className="flex items-end">
            <button
              type="submit"
              className="w-full rounded-lg bg-blue-600 px-4 py-3 font-semibold hover:bg-blue-700"
            >
              Search Trains
            </button>
          </div>

          {/* Show All */}
          <button
            type="button"
            onClick={showAllTrains}
            className="rounded-lg border border-gray-700 px-4 py-3 font-semibold hover:bg-gray-800 md:col-span-3"
          >
            Show All Trains
          </button>

        </form>

        {/* ================= MESSAGE ================= */}

        {message && (
          <p className="mt-6 text-center text-gray-300">
            {message}
          </p>
        )}

        {/* ================= BOOKING SUCCESS ================= */}

        {bookingSuccess && (
          <div className="mt-8 rounded-2xl border border-green-700 bg-green-950 p-6">

            <h2 className="text-2xl font-bold text-green-400">
              Ticket Booked Successfully
            </h2>

            <div className="mt-4 space-y-2 text-gray-200">

              <p>
                <strong>PNR:</strong>{" "}
                {bookingSuccess.pnr}
              </p>

              <p>
                <strong>Train:</strong>{" "}
                {bookingSuccess.train}
              </p>

              <p>
                <strong>Passenger:</strong>{" "}
                {bookingSuccess.passenger}
              </p>

              <p>
                <strong>Journey Date:</strong>{" "}
                {bookingSuccess.journeyDate}
              </p>

              <p>
                <strong>Fare:</strong>{" "}
                ₹{bookingSuccess.fare}
              </p>

            </div>

          </div>
        )}

        {/* ================= LOADING ================= */}

        {loading && (
          <p className="mt-8 text-center text-gray-400">
            Loading trains...
          </p>
        )}

        {/* ================= TRAIN CARDS ================= */}

        {!loading && trains.length > 0 && (
          <div className="mt-8 grid gap-5 md:grid-cols-2">

            {trains.map((train) => (
              <div
                key={train.TRAIN_ID}
                className="rounded-2xl border border-gray-800 bg-gray-900 p-6"
              >

                <div className="flex items-start justify-between">

                  <div>
                    <p className="text-sm text-blue-400">
                      {train.TRAIN_NUMBER}
                    </p>

                    <h2 className="mt-1 text-xl font-bold">
                      {train.TRAIN_NAME}
                    </h2>
                  </div>

                  <p className="text-lg font-bold">
                    ₹{train.FARE}
                  </p>

                </div>

                <div className="mt-6 flex items-center gap-4">

                  <div>
                    <p className="text-xs text-gray-500">
                      FROM
                    </p>

                    <p className="font-semibold">
                      {train.SOURCE}
                    </p>
                  </div>

                  <div className="flex-1 border-t border-dashed border-gray-700" />

                  <div className="text-right">
                    <p className="text-xs text-gray-500">
                      TO
                    </p>

                    <p className="font-semibold">
                      {train.DESTINATION}
                    </p>
                  </div>

                </div>

                <button
                  onClick={() => openBooking(train)}
                  className="mt-6 w-full rounded-lg bg-green-600 px-4 py-3 font-semibold hover:bg-green-700"
                >
                  Book Ticket
                </button>

              </div>
            ))}

          </div>
        )}

        {!loading &&
          trains.length === 0 &&
          !message && (
            <p className="mt-8 text-center text-gray-400">
              No trains available.
            </p>
          )}

      </div>

      {/* ================= BOOKING MODAL ================= */}

      {selectedTrain && (
        <div className="fixed inset-0 z-50 flex items-center justify-center bg-black/70 px-4">

          <div className="w-full max-w-lg rounded-2xl bg-gray-900 p-6">

            {/* Modal Header */}

            <div className="flex items-center justify-between">

              <div>
                <p className="text-sm text-blue-400">
                  {selectedTrain.TRAIN_NUMBER}
                </p>

                <h2 className="text-2xl font-bold">
                  {selectedTrain.TRAIN_NAME}
                </h2>
              </div>

              <button
                type="button"
                onClick={() => setSelectedTrain(null)}
                className="text-2xl text-gray-400 hover:text-white"
              >
                ×
              </button>

            </div>

            <p className="mt-2 text-gray-400">
              {selectedTrain.SOURCE} →{" "}
              {selectedTrain.DESTINATION}
            </p>

            {/* Booking Form */}

            <form
              onSubmit={handleBooking}
              className="mt-6 space-y-5"
            >

              {/* Passenger Name */}

              <div>
                <label className="mb-2 block text-sm font-medium text-gray-300">
                  Passenger Name
                </label>

                <input
                  type="text"
                  placeholder="Enter passenger name"
                  value={passengerName}
                  onChange={(e) =>
                    setPassengerName(e.target.value)
                  }
                  required
                  className="w-full rounded-lg border border-gray-700 bg-gray-800 px-4 py-3 text-white outline-none focus:border-blue-500"
                />
              </div>

              {/* Age */}

              <div>
                <label className="mb-2 block text-sm font-medium text-gray-300">
                  Age
                </label>

                <input
                  type="number"
                  placeholder="Enter passenger age"
                  min="1"
                  max="120"
                  value={age}
                  onChange={(e) =>
                    setAge(e.target.value)
                  }
                  required
                  className="w-full rounded-lg border border-gray-700 bg-gray-800 px-4 py-3 text-white outline-none focus:border-blue-500"
                />
              </div>

              {/* Gender */}

              <div>
                <label className="mb-2 block text-sm font-medium text-gray-300">
                  Gender
                </label>

                <select
                  value={gender}
                  onChange={(e) =>
                    setGender(e.target.value)
                  }
                  required
                  className="w-full rounded-lg border border-gray-700 bg-gray-800 px-4 py-3 text-white outline-none focus:border-blue-500"
                >
                  <option value="">
                    Select gender
                  </option>

                  <option value="Male">
                    Male
                  </option>

                  <option value="Female">
                    Female
                  </option>

                  <option value="Other">
                    Other
                  </option>
                </select>
              </div>

              {/* Journey Date */}

              <div>
                <label className="mb-2 block text-sm font-medium text-gray-300">
                  Journey Date
                </label>

                <input
                  type="date"
                  value={journeyDate}
                  onChange={(e) =>
                    setJourneyDate(e.target.value)
                  }
                  required
                  className="w-full rounded-lg border border-gray-700 bg-gray-800 px-4 py-3 text-white outline-none focus:border-blue-500"
                />
              </div>

              {/* Confirm Booking */}

              <button
                type="submit"
                disabled={bookingLoading}
                className="w-full rounded-lg bg-green-600 px-4 py-3 font-semibold hover:bg-green-700 disabled:opacity-50"
              >
                {bookingLoading
                  ? "Booking..."
                  : "Confirm Booking"}
              </button>

            </form>

          </div>

        </div>
      )}

    </main>
  );
}