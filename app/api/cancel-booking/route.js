import { NextResponse } from "next/server";
import { getConnection } from "@/lib/oracle";

export async function PUT(request) {
  let connection;

  try {
    const { bookingId, userId } = await request.json();

    if (!bookingId || !userId) {
      return NextResponse.json({
        success: false,
        message: "Booking ID and User ID are required",
      });
    }

    connection = await getConnection();

    // Find the booking
    const bookingResult = await connection.execute(
      `
      SELECT booking_id, train_id, status
      FROM bookings
      WHERE booking_id = :bookingId
      AND user_id = :userId
      `,
      {
        bookingId,
        userId,
      }
    );

    if (bookingResult.rows.length === 0) {
      return NextResponse.json({
        success: false,
        message: "Booking not found",
      });
    }

    const booking = bookingResult.rows[0];

    // Check whether already cancelled
    if (booking.STATUS === "CANCELLED") {
      return NextResponse.json({
        success: false,
        message: "Booking is already cancelled",
      });
    }

    // Cancel booking
    await connection.execute(
      `
      UPDATE bookings
      SET status = 'CANCELLED'
      WHERE booking_id = :bookingId
      `,
      {
        bookingId,
      }
    );

    // Restore one seat
    await connection.execute(
      `
      UPDATE trains
      SET available_seats = available_seats + 1
      WHERE train_id = :trainId
      `,
      {
        trainId: booking.TRAIN_ID,
      }
    );

    await connection.commit();

    return NextResponse.json({
      success: true,
      message: "Booking cancelled successfully",
    });

  } catch (error) {
    console.error("Cancel Booking Error:", error);

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