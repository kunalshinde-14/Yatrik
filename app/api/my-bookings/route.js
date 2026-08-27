import { NextResponse } from "next/server";
import { getConnection } from "@/lib/oracle";

export async function GET(request) {
  let connection;

  try {
    const { searchParams } = new URL(request.url);
    const userId = searchParams.get("userId");

    if (!userId) {
      return NextResponse.json({
        success: false,
        message: "User ID is required",
      });
    }

    connection = await getConnection();

    const result = await connection.execute(
      `
      SELECT
        b.booking_id,
        b.pnr,
        b.passenger_name,
        b.age,
        b.gender,
        b.journey_date,
        b.status,
        t.train_number,
        t.train_name,
        t.source,
        t.destination,
        t.fare
      FROM bookings b
      INNER JOIN trains t
        ON b.train_id = t.train_id
      WHERE b.user_id = :userId
      ORDER BY b.booking_id DESC
      `,
      { userId }
    );

    return NextResponse.json({
      success: true,
      data: result.rows,
    });

  } catch (error) {
    console.error("My Bookings Error:", error);

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