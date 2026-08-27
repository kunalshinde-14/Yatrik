import { NextResponse } from "next/server";
import { getConnection } from "@/lib/oracle";

export async function POST(request) {
  let connection;

  try {
    const {
      userId,
      trainId,
      passengerName,
      age,
      gender,
      journeyDate,
    } = await request.json();

    // Check required fields
    if (
      !userId ||
      !trainId ||
      !passengerName ||
      !age ||
      !gender ||
      !journeyDate
    ) {
      return NextResponse.json({
        success: false,
        message: "All fields are required",
      });
    }

    connection = await getConnection();

    // Check if train exists
    const trainResult = await connection.execute(
      `SELECT train_id, train_name, fare, available_seats
       FROM trains
       WHERE train_id = :trainId`,
      { trainId }
    );

    if (trainResult.rows.length === 0) {
      return NextResponse.json({
        success: false,
        message: "Train not found",
      });
    }

    const train = trainResult.rows[0];

    // Check available seats
    if (train.AVAILABLE_SEATS <= 0) {
      return NextResponse.json({
        success: false,
        message: "No seats available",
      });
    }

    // Generate PNR
    const pnr = "YAT" + Date.now();

    // Insert booking
    await connection.execute(
      `INSERT INTO bookings
       (
         user_id,
         train_id,
         passenger_name,
         age,
         gender,
         journey_date,
         pnr,
         status
       )
       VALUES
       (
         :userId,
         :trainId,
         :passengerName,
         :age,
         :gender,
         TO_DATE(:journeyDate, 'YYYY-MM-DD'),
         :pnr,
         'CONFIRMED'
       )`,
      {
        userId,
        trainId,
        passengerName,
        age,
        gender,
        journeyDate,
        pnr,
      }
    );

    // Reduce available seats
    await connection.execute(
      `UPDATE trains
       SET available_seats = available_seats - 1
       WHERE train_id = :trainId`,
      { trainId }
    );

    // Save changes
    await connection.commit();

    return NextResponse.json({
      success: true,
      message: "Ticket booked successfully",
      pnr: pnr,
      train: train.TRAIN_NAME,
      passenger: passengerName,
      journeyDate: journeyDate,
      fare: train.FARE,
    });

  } catch (error) {
    console.error("Booking Error:", error);

    if (connection) {
      await connection.rollback();
    }

    return NextResponse.json({
      success: false,
      message: error.message,
    });

  } finally {
    if (connection) {
      await connection.close();
    }
  }
}